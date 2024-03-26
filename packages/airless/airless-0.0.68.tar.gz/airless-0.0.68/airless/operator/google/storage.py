
import os
import logging
from datetime import datetime, timedelta, timezone
import copy

from google.api_core.exceptions import NotFound
import pyarrow as pa
from pyarrow import parquet
from pyarrow import fs

from airless.config import get_config
from airless.hook.google.bigquery import BigqueryHook
from airless.hook.google.storage import GcsHook
from airless.hook.file.file import FileHook
from airless.operator.base import BaseFileOperator, BaseEventOperator


class ProcessTopic:
    SMALL = 'PUBSUB_TOPIC_FILE_BATCH_AGGREGATE_PROCESS_SMALL'
    MEDIUM = 'PUBSUB_TOPIC_FILE_BATCH_AGGREGATE_PROCESS_MEDIUM'
    LARGE = 'PUBSUB_TOPIC_FILE_BATCH_AGGREGATE_PROCESS_LARGE'


class FileDetectOperator(BaseFileOperator):

    def __init__(self):
        super().__init__()
        self.gcs_hook = GcsHook()

    def execute(self, bucket, filepath):
        success_messages = self.build_success_message(bucket, filepath)

        for success_message in success_messages:
            self.pubsub_hook.publish(
                project=get_config('GCP_PROJECT'),
                topic=get_config('PUBSUB_TOPIC_FILE_TO_BQ'),
                data=success_message)

    def build_success_message(self, bucket, filepath):
        dataset, table, mode, separator, skip_leading_rows, \
            file_format, schema, run_next, quote_character, encoding, \
            column_names, time_partitioning, processing_method, \
            gcs_table_name, sheet_name, arguments, options = self.get_ingest_config(filepath)

        metadatas = []
        for idx in range(len(file_format)):
            metadatas.append({
                'metadata': {
                    'destination_dataset': dataset,
                    'destination_table': table,
                    'file_format': file_format[idx],
                    'mode': mode,
                    'bucket': bucket,
                    'file': filepath,
                    'separator': separator[idx],
                    'skip_leading_rows': skip_leading_rows[idx],
                    'quote_character': quote_character[idx],
                    'encoding': encoding[idx],
                    'schema': schema[idx],
                    'run_next': run_next[idx],
                    'column_names': column_names[idx],
                    'time_partitioning': time_partitioning[idx],
                    'processing_method': processing_method[idx],
                    'gcs_table_name': gcs_table_name[idx],
                    'sheet_name': sheet_name[idx],
                    'arguments': arguments[idx],
                    'options': options[idx]
                }
            })

        return metadatas

    def get_ingest_config(self, filepath):
        dataset, table, mode = self.split_filepath(filepath)

        metadata = self.read_config_file(dataset, table)

        # Verifying if config file hava multiple configs or not
        if isinstance(metadata, list):
            metadata = metadata
        elif isinstance(metadata, dict):
            metadata = [metadata]
        else:
            raise NotImplementedError()

        # Instanciate all values
        # inputs
        file_format = []
        separator = []
        skip_leading_rows = []
        quote_character = []
        encoding = []
        sheet_name = []
        arguments = []
        options = []

        # outputs
        schema = []
        column_names = []
        time_partitioning = []
        processing_method = []
        gcs_table_name = []
        run_next = []

        for config in metadata:
            # input
            file_format.append(config.get('file_format', 'csv'))
            separator.append(config.get('separator'))
            skip_leading_rows.append(config.get('skip_leading_rows'))
            quote_character.append(config.get('quote_character'))
            encoding.append(config.get('encoding', None))
            sheet_name.append(config.get('sheet_name', None))
            arguments.append(config.get('arguments', None))
            options.append(config.get('options', None))

            # output
            schema.append(config.get('schema', None))
            column_names.append(config.get('column_names', None))
            time_partitioning.append(config.get('time_partitioning', None))
            processing_method.append(config.get('processing_method', None))
            gcs_table_name.append(config.get('gcs_table_name', None))

            # after processing
            run_next.append(config.get('run_next', []))

        return dataset, table, mode, separator, \
            skip_leading_rows, file_format, schema, \
            run_next, quote_character, encoding, column_names, \
            time_partitioning, processing_method, gcs_table_name, \
            sheet_name, arguments, options

    def split_filepath(self, filepath):
        filepath_array = filepath.split('/')
        if len(filepath_array) < 3:
            raise Exception('Invalid file path. Must be added to directory {dataset}/{table}/{mode}')

        dataset = filepath_array[0]
        table = filepath_array[1]
        mode = filepath_array[2]
        return dataset, table, mode

    def read_config_file(self, dataset, table):
        try:
            config = self.gcs_hook.read_json(
                bucket=get_config('GCS_BUCKET_LANDING_ZONE_LOADER_CONFIG'),
                filepath=f'{dataset}/{table}.json')
            return config
        except NotFound:
            return {'file_format': 'json', 'time_partitioning': {'type': 'DAY', 'field': '_created_at'}}


class FileToBigqueryOperator(BaseEventOperator):

    def __init__(self):
        super().__init__()
        self.gcs_hook = GcsHook()
        self.bigquery_hook = BigqueryHook()

    def execute(self, data, topic):
        metadata = data['metadata']
        file_format = metadata['file_format']

        if file_format in ('csv', 'json'):
            self.bigquery_hook.load_file(
                from_filepath=self.gcs_hook.build_filepath(metadata['bucket'], metadata['file']),
                from_file_format=file_format,
                from_separator=metadata.get('separator'),
                from_skip_leading_rows=metadata.get('skip_leading_rows'),
                from_quote_character=metadata.get('quote_character'),
                from_encoding=metadata.get('encoding'),
                to_project=get_config('GCP_PROJECT'),
                to_dataset=metadata['destination_dataset'],
                to_table=metadata['destination_table'],
                to_mode=metadata['mode'],
                to_schema=metadata.get('schema'),
                to_time_partitioning=metadata.get('time_partitioning'))

        else:
            raise Exception(f'File format {file_format} load not implemented')


class BatchWriteDetectOperator(BaseEventOperator):
    # Will be deprecreated

    def __init__(self):
        super().__init__()
        self.file_hook = FileHook()
        self.gcs_hook = GcsHook()

    def execute(self, data, topic):
        bucket = data.get('bucket', get_config('GCS_BUCKET_LANDING_ZONE'))
        prefix = data.get('prefix')
        threshold = data['threshold']

        tables = {}
        partially_processed_tables = []

        for b in self.gcs_hook.list(bucket, prefix):
            if b.time_deleted is None:
                filepaths = b.name.split('/')
                key = '/'.join(filepaths[:-1])  # dataset/table
                filename = filepaths[-1]

                if tables.get(key) is None:
                    tables[key] = {
                        'size': b.size,
                        'files': [filename],
                        'min_time_created': b.time_created
                    }
                else:
                    tables[key]['size'] += b.size
                    tables[key]['files'] += [filename]
                    if b.time_created < tables[key]['min_time_created']:
                        tables[key]['min_time_created'] = b.time_created

                if (tables[key]['size'] > threshold['size']) or (len(tables[key]['files']) > threshold['file_quantity']):
                    self.send_to_process(bucket=bucket, directory=key, files=tables[key]['files'])
                    tables[key] = None
                    partially_processed_tables.append(key)

        # verify which dataset/table is ready to be processed
        time_threshold = (datetime.now() - timedelta(minutes=threshold['minutes'])).strftime('%Y-%m-%d %H:%M')
        for directory, v in tables.items():
            if v is not None:
                if (v['size'] > threshold['size']) or \
                    (v['min_time_created'].strftime('%Y-%m-%d %H:%M') < time_threshold) or \
                        (len(v['files']) > threshold['file_quantity']) or \
                        (directory in partially_processed_tables):
                    self.send_to_process(bucket=bucket, directory=directory, files=v['files'])

    def send_to_process(self, bucket, directory, files):
        self.pubsub_hook.publish(
            project=get_config('GCP_PROJECT'),
            topic=get_config('PUBSUB_TOPIC_BATCH_WRITE_PROCESS'),
            data={'bucket': bucket, 'directory': directory, 'files': files})


class BatchWriteDetectAggregateOperator(BaseEventOperator):

    def __init__(self):
        super().__init__()
        self.file_hook = FileHook()
        self.gcs_hook = GcsHook()
        self.reprocess = False
        self.document_db_folder = 'batch-write-detect-aggregate'

        self.tables_last_timestamp_processed = {}
        self.tables = {}
        self.partially_processed_tables = []

    def execute(self, data, topic):
        config = {
            "bucket": data.get('bucket', get_config('GCS_BUCKET_LANDING_ZONE')),
            "prefix": data.get('prefix'),
            "threshold": data['threshold'],
            "reprocess_time": data.get('metadata', {}).get('reprocess_time', 0)
        }
        deadline = config["threshold"].get('deadline_files_to_process', 60)  # minutes
        reprocess_delay = config["threshold"].get('reprocess_delay', 60)  # seconds
        reprocess_max_times = config["threshold"].get('reprocess_max_times', 0)

        self.process_files(config, deadline)
        self.verify_processed_tables(config)

        if self.reprocess and config["reprocess_time"] < reprocess_max_times:
            self.send_to_reprocess(reprocess_delay, topic, data)

    def process_files(self, config, deadline):
        # blobs = list(self.gcs_hook.list(config["bucket"], config["prefix"]))
        # blobs.sort(key=lambda x: x.time_created)

        # for blob in blobs:

        for blob in self.gcs_hook.list(config["bucket"], config["prefix"]):
            table_key, filename = self.decompose_uri(blob.name)
            last_timestamp = self.verify_table_last_timestamp_processed(table_key)

            if self.is_processing_required(blob, last_timestamp, deadline) and filename:
                self.update_table_records(blob, table_key, filename)
                self.check_and_send_for_processing(table_key, config)

    def is_processing_required(self, blob, last_timestamp, deadline):
        current_time = datetime.now(timezone.utc)
        return blob.time_deleted is None and (
            blob.time_created > last_timestamp or blob.time_created < current_time - timedelta(minutes=deadline)
        )

    def update_table_records(self, blob, table_key, filename):
        self.tables.setdefault(table_key, {
            'size': 0,
            'files': [],
            'min_time_created': datetime(2300, 1, 1, 12, 12, 12).replace(tzinfo=timezone.utc),
            'max_time_created': datetime(1900, 1, 1, 12, 12, 12).replace(tzinfo=timezone.utc)
        })

        self.tables[table_key]['size'] += blob.size
        self.tables[table_key]['files'].append(filename)
        self.tables[table_key]['min_time_created'] = min(self.tables[table_key]['min_time_created'], blob.time_created)
        self.tables[table_key]['max_time_created'] = max(self.tables[table_key]['max_time_created'], blob.time_created)

    def check_and_send_for_processing(self, table_key, config):
        if self.tables[table_key]['size'] > config["threshold"]['size_medium']:
            self.process_and_reset_table(table_key, config["bucket"], get_config('GCS_BUCKET_RAW_ZONE'), ProcessTopic.MEDIUM)
        elif len(self.tables[table_key]['files']) > config["threshold"]['file_quantity']:
            size = ProcessTopic.SMALL if self.tables[table_key]['size'] < config["threshold"]['size_small'] else ProcessTopic.MEDIUM
            self.process_and_reset_table(table_key, config["bucket"], config["bucket"], size)

    def process_and_reset_table(self, table_key, from_bucket, to_bucket, size):
        self.send_to_process(from_bucket, to_bucket, table_key, self.tables[table_key]['files'], size)
        self.tables[table_key] = {
            'size': 0,
            'files': [],
            'min_time_created': self.tables[table_key]['min_time_created'],
            'max_time_created': self.tables[table_key]['max_time_created']
        }
        self.partially_processed_tables.append(table_key)

    def verify_processed_tables(self, config):
        time_threshold = datetime.now(timezone.utc) - timedelta(minutes=config["threshold"]['minutes'])
        for directory, data in self.tables.items():
            if data['files']:
                self.process_based_on_file_count(directory, data, config, time_threshold)

            self.update_last_timestamp(directory, data)

    def process_based_on_file_count(self, directory, data, config, time_threshold):
        if len(data['files']) == 1 and directory not in self.partially_processed_tables:
            # only have one file that is lower than best performnce partition size in this directory
            size = ProcessTopic.SMALL if data['size'] < config["threshold"]['size_small'] else ProcessTopic.MEDIUM
            self.send_to_process(config["bucket"], get_config('GCS_BUCKET_RAW_ZONE'), directory, data['files'], size)
        elif directory in self.partially_processed_tables or data['min_time_created'] < time_threshold:
            size = ProcessTopic.SMALL if data['size'] < config["threshold"]['size_small'] else ProcessTopic.MEDIUM
            self.send_to_process(config["bucket"], config["bucket"], directory, data['files'], size)

    def update_last_timestamp(self, directory, data):
        dataset, table = self.decompose_uri(directory)
        self.gcs_hook.upload_from_memory(
            data={'processed_at': data['max_time_created'].strftime('%Y%m%d%H%M%S')},
            bucket=get_config('GCS_BUCKET_DOCUMENT_DB'),
            directory=f'{self.document_db_folder}/{dataset}',
            filename=f'{table}.json',
            add_timestamp=False)

    def verify_table_last_timestamp_processed(self, directory):
        logging.debug(f"Verify table last timestamp processed for {self.document_db_folder}/{directory}")
        if directory in self.tables_last_timestamp_processed.keys():
            logging.debug('Get timestamp from memory')
            return self.tables_last_timestamp_processed[directory]
        else:
            logging.debug(f"Get timestamp from bucket {get_config('GCS_BUCKET_DOCUMENT_DB')} dataset {self.document_db_folder}/{directory}")
            try:
                dataset, table = self.decompose_uri(directory)
                info = self.gcs_hook.read_json(get_config('GCS_BUCKET_DOCUMENT_DB'), f'{self.document_db_folder}/{dataset}/{table}.json')
                timestamp = info['processed_at']
                timestamp_obj = datetime.strptime(timestamp, '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
            except NotFound:
                timestamp_obj = datetime(1900, 1, 1, 12, 12, 12).replace(tzinfo=timezone.utc)

            self.tables_last_timestamp_processed[directory] = timestamp_obj
            return timestamp_obj

    def decompose_uri(self, filepath):
        dataset = '/'.join(filepath.split('/')[:-1])
        table = filepath.split('/')[-1]

        return dataset, table

    def send_to_process(self, from_bucket, to_bucket, directory, files, size):
        self.pubsub_hook.publish(
            project=get_config('GCP_PROJECT'),
            topic=get_config(size),
            data={'from_bucket': from_bucket, 'to_bucket': to_bucket, 'directory': directory, 'files': files})

        self.reprocess = True

    def send_to_reprocess(self, reprocess_delay, topic, data):
        reprocess_data = copy.deepcopy(data)

        reprocess_data['threshold']['minutes'] = 0  # Change to zero because new files were aggreagated
        reprocess_data.setdefault('metadata', {}).setdefault('reprocess_time', 0)  # Ensurse metadata and reprocess_time exists
        reprocess_data['metadata']['reprocess_time'] += 1

        self.pubsub_hook.publish(
            project=get_config('GCP_PROJECT'),
            topic=get_config('PUBSUB_DELAY_TOPIC'),
            data={'seconds': reprocess_delay, 'metadata': {'run_next': [{'topic': topic, 'data': reprocess_data}]}})


class BatchWriteProcessOperator(BaseEventOperator):

    def __init__(self):
        super().__init__()
        self.file_hook = FileHook()
        self.gcs_hook = GcsHook()

    def execute(self, data, topic):
        from_bucket = data['bucket']
        directory = data['directory']
        files = data['files']

        file_contents = self.read_files(from_bucket, directory, files)

        local_filepath = self.merge_files(file_contents)

        self.gcs_hook.upload(local_filepath, get_config('GCS_BUCKET_LANDING_ZONE_LOADER'), f'{directory}/append')
        os.remove(local_filepath)

        file_paths = [directory + '/' + f for f in files]

        self.gcs_hook.move_files(
            from_bucket=from_bucket,
            files=file_paths,
            to_bucket=get_config('GCS_BUCKET_LANDING_ZONE_PROCESSED'),
            to_directory=directory,
            rewrite=False
        )

    def read_files(self, bucket, directory, files):
        file_contents = []
        for f in files:
            obj = self.gcs_hook.read_json(
                bucket=bucket,
                filepath=f'{directory}/{f}')
            if isinstance(obj, list):
                file_contents += obj
            elif isinstance(obj, dict):
                file_contents.append(obj)
            else:
                raise Exception(f'Cannot process file {directory}/{f}')
        return file_contents

    def merge_files(self, file_contents):
        local_filepath = self.file_hook.get_tmp_filepath('merged.ndjson', add_timestamp=True)
        self.file_hook.write(local_filepath=local_filepath, data=file_contents, use_ndjson=True)
        return local_filepath


class BatchAggregateParquetFilesOperator(BaseEventOperator):
    def __init__(self):
        super().__init__()
        self.file_hook = FileHook()
        self.gcs_hook = GcsHook()
        self.fs_gcs = fs.GcsFileSystem()

    def execute(self, data, topic):
        from_bucket = data['from_bucket']
        to_bucket = data['to_bucket']
        directory = data['directory']
        files = data['files']

        # Read parquets from gcs
        tables_union = self.read_parquet_from_gcs(from_bucket, directory, files)

        # Save parquet concatenated
        local_filename = self.file_hook.get_tmp_filepath('tmp.parquet', add_timestamp=True)
        local_filename = local_filename.split('/')[-1]
        parquet.write_table(
            tables_union,
            f'{to_bucket}/{directory}/{local_filename}',
            compression='GZIP',
            filesystem=self.fs_gcs
        )

        self.send_to_delete(from_bucket, directory, files)

    def read_parquet_from_gcs(self, bucket, directory, files):
        concat = None
        for f in files:
            t = parquet.read_table(f'{bucket}/{directory}/{f}', filesystem=self.fs_gcs)
            concat = t if not concat else pa.concat_tables([t, concat])

        return concat

    def send_to_delete(self, from_bucket, directory, files):
        obj = {
            'bucket': from_bucket,
            'files': [f'{directory}/{f}' for f in files]
        }

        self.pubsub_hook.publish(
            project=get_config('GCP_PROJECT'),
            topic=get_config('PUBSUB_TOPIC_GCS_DELETE'),
            data=obj)


class FileDeleteOperator(BaseEventOperator):

    def __init__(self):
        super().__init__()
        self.gcs_hook = GcsHook()

    def execute(self, data, topic):
        bucket = data['bucket']
        prefix = data.get('prefix')
        files = data.get('files', [])

        if (prefix is None) and (not files):
            raise Exception('prefix or files parameter has to be defined!')

        logging.info(f'Deleting from bucket {bucket}')
        self.gcs_hook.delete(bucket, prefix, files)


class FileMoveOperator(BaseEventOperator):

    def __init__(self):
        super().__init__()
        self.gcs_hook = GcsHook()

    def execute(self, data, topic):
        origin_bucket = data['origin']['bucket']
        origin_prefix = data['origin']['prefix']
        dest_bucket = data['destination']['bucket']
        dest_directory = data['destination']['directory']
        self.gcs_hook.move(origin_bucket, origin_prefix, dest_bucket, dest_directory, True)
