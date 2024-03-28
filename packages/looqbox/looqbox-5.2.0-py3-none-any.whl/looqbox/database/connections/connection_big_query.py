import os
import re
import warnings
from hashlib import md5
from uuid import uuid4

from multimethod import multimethod

from looqbox.utils.utils import open_file
from looqbox.database.connections.connection_base import BaseConnection
from google.cloud.bigquery import enums, QueryJobConfig
from google.api_core.exceptions import NotFound
from looqbox.global_calling import GlobalCalling
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import json
import datetime
from time import sleep


TABLE_NAME_REGEX_PATTERN = re.compile(r"""(?<!as\W`|AS\W`)(?<=`)(.+)(?=`)""", re.IGNORECASE)


class BigQueryConnection(BaseConnection):
    def __init__(self, connection_name: str, **additional_args):
        super().__init__()
        self.connection_alias = connection_name
        self.connection_object = dict()
        self.response_timeout = GlobalCalling.looq.response_timeout if not self.test_mode else 0
        self.eval_limit = 10
        self.search_for_job_id_limit = 10

    def set_query_script(self, sql_script: str) -> None:
        self.query = sql_script

    def connect(self):
        self.connection_object = self._get_connection_credentials(self.connection_alias)
        big_query_key = json.loads(self.connection_object.get("apiKey"))
        return self._connect_to_client(big_query_key)

    def _get_connection_credentials(self, connection: str, parameter_as_json=False) -> dict:
        """
        Get credentials for a list of connections.

        :param connection: String of database names
        :param parameter_as_json: Set if the parameters will be in JSON format or not
        :return: A Connection object
        """

        connection_credential = self._get_connection_file()
        try:
            if not parameter_as_json:
                connection_credential = GlobalCalling.looq.connection_config[connection]
            else:
                connection_credential = connection_credential[connection]
        except KeyError:
            raise Exception(
                "Connection " + connection + " not found in the file " + GlobalCalling.looq.connection_file)

        return connection_credential

    def _call_query_executor(self, start_time, query_mode="single"):
        try:
            self._get_query_result()
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query(
                self.build_log(
                    time=str(total_sql_time),
                    success=True,
                    mode=query_mode
                )
            )
            self._update_response_timeout(total_sql_time)

        except Exception as execution_error:

            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=False,
                                                   mode=query_mode)
                                    )

            raise execution_error

    def _execute_query(self, bq_client):

        self._set_search_job_id_interval_time()
        query_request = {"query": self.query, "useLegacySql": False}

        query_request["location"] = self._get_table_location(bq_client)
        bq_response = bq_client._connection.api_request(
            "POST",
            f"/projects/{bq_client.project}/queries",
            data=query_request
        )

        job_complete = bq_response.get("jobComplete", False)
        job_id = bq_response.get("jobReference", {}).get("jobId")
        page_token = bq_response.get("pageToken")

        if not job_complete:
            bq_response = self._wait_for_job_to_complete(bq_client, job_id)

        search_for_job_id_attempts = 0
        while page_token is not None:
            try:
                rows = bq_response.get("rows", [])

                page_response = self._get_response_by_job_id(bq_client, job_id,
                                                             {"pageToken": page_token})
                page_rows = page_response.get("rows", [])
                rows.extend(page_rows)
                bq_response["rows"] = rows
                page_token = page_response.get("pageToken")

            except NotFound as job_no_found_exception:
                search_for_job_id_attempts += 1
                if search_for_job_id_attempts >= self.search_for_job_id_limit:
                    break

                warnings.warn(str(job_no_found_exception))
                sleep(self.interval_time)

        return bq_response

    def _get_table_location(self, bq_client):

        table_name = self._get_table_name_from_query()
        dataset_location = None
        if table_name:
            dataset_info = bq_client.get_table(table_name)
            dataset_location = dataset_info.location
        # TODO replace hardcoded default with class.configuration_options
        return dataset_location or "southamerica-east1"

    def _get_table_name_from_query(self):

        import re
        table_name = re.search(TABLE_NAME_REGEX_PATTERN, self.query)
        try:
            return table_name.group(0)
        except AttributeError:
            return None

    def _wait_for_job_to_complete(self, bq_client, job_id):

        bq_response = self._get_response_by_job_id(bq_client, job_id)
        job_complete = bq_response.get("jobComplete", False) if bq_response is not None else False
        search_for_job_id_attempts = 0
        while not job_complete or search_for_job_id_attempts <= self.eval_limit:
            bq_response = self._get_response_by_job_id(bq_client, job_id)
            job_complete = bq_response.get("jobComplete", False) if bq_response is not None else False
            search_for_job_id_attempts += 1
            sleep(self.interval_time)

        if not job_complete:
            raise Exception("Job did not complete in time")

        return bq_response

    def _get_response_by_job_id(self, bq_client, job_id, query_params=None):

        bq_response = None
        if query_params is None:
            query_params = {}

        if not bq_client.location:
            query_params = {"location": "southamerica-east1"}

        search_for_job_id_attempts = 0
        while search_for_job_id_attempts <= self.search_for_job_id_limit:
            try:
                bq_response = bq_client._connection.api_request(
                    "GET",
                    f"/projects/{bq_client.project}/queries/{job_id}",
                    query_params=query_params
                )
                return bq_response
            except NotFound as job_no_found_exception:
                search_for_job_id_attempts += 1
                warnings.warn(str(job_no_found_exception))
                sleep(self.interval_time)
        return bq_response

    def _set_search_job_id_interval_time(self):

        connection_configuration_file = open_file(
            os.path.dirname(__file__), "..", "..", "configuration", "database_connection_settings.json"
        )
        connection_configuration = json.load(connection_configuration_file)
        connection_configuration_file.close()

        self.interval_time = connection_configuration.get("searchJobIdIntervalTime", 0.0005)

    def _build_dataframe_from_response(self, response):

        fields = response.get("schema").get("fields")
        rows = response.get("rows") or []
        column_names = [field.get("name") for field in fields]
        column_types = [field.get("type") for field in fields]
        type_dict = dict(zip(column_names, column_types))
        row_list = [row.get("f") for row in rows]
        raw_data_frame = pd.DataFrame(data=row_list, columns=column_names)
        data_frame = raw_data_frame.applymap(lambda cell: cell.get("v"))
        self._convert_columns_type(data_frame, type_dict)
        return data_frame

    def _execute_query_for_large_dataset(self, bq_client):

        config = QueryJobConfig()
        config.use_legacy_sql = False
        api_query_method = enums.QueryApiMethod.QUERY

        bq_response = bq_client.query(self.query, job_config=config, api_method=api_query_method)
        column_schemas = {sche._properties["name"]: sche._properties["type"] for sche in bq_response.schema}

        bq_arrow_response = bq_response.to_arrow()
        bq_response_dataframe = bq_arrow_response.to_pandas()
        bq_response_dataframe = self._convert_columns_type(bq_response_dataframe, column_schemas)
        return bq_response_dataframe

    def _get_query_result(self):
        bq_client = self.connect()

        if self.is_optimized_for_large_dataset:
            self.retrieved_data = self._execute_query_for_large_dataset(bq_client)
            self.query_metadata = self._get_metadata_from_dataframe(self.retrieved_data)

        else:
            bq_response = self._execute_query(bq_client)
            self.retrieved_data = self._build_dataframe_from_response(bq_response)
            self.query_metadata = self.get_table_metadata_from_request(bq_response)

    @staticmethod
    def _connect_to_client(big_query_key):
        credentials = service_account.Credentials.from_service_account_info(
            big_query_key, scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/bigquery"
            ]
        )
        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id
            # location=["southamerica-east1", "US"]
        )
        return client

    def _convert_columns_type(self, data_frame, types):
        type_function_map = {
            "NUMERIC": "float",
            "BIGNUMERIC": "float",
            "FLOAT": "float",
            "INTEGER": "int",
            "RECORD": "json_normalize",
            "TIMESTAMP": "datetime64[ns]",
        }
        for column, data_type in types.items():
            if type_function_map.get(data_type):
                astype_type = type_function_map[data_type]
                if astype_type == "int":
                    data_frame[column] = data_frame[column].astype("int", errors="ignore")
                    if data_frame[column].dtype != astype_type:
                        data_frame[column] = data_frame[column].astype("float")
                    data_frame[column] = data_frame[column].astype(astype_type, errors="ignore")
                elif astype_type == "json_normalize":
                    # TODO fix column order
                    normalized_df = pd.json_normalize(data_frame[column])
                    normalized_df.columns = [f"{column}.{sub_column}" for sub_column in normalized_df.columns]
                    data_frame = self.insert_normalized_columns(column, normalized_df, data_frame)
                else:
                    data_frame[column] = data_frame[column].astype(astype_type, errors="ignore")
        return data_frame

    def insert_normalized_columns(self, column: str, normalized_dataframe: pd.DataFrame,
                                  original_data_frame: pd.DataFrame) -> pd.DataFrame:
        original_column_position = original_data_frame.columns.get_loc(column)
        column_insertion = original_column_position + 1
        for new_column in normalized_dataframe.columns:
            original_data_frame.insert(column_insertion, new_column,
                                       normalized_dataframe[new_column])
            column_insertion += 1

        completed_dataframe = original_data_frame.drop(columns=[column])
        return completed_dataframe

    @staticmethod
    def get_table_metadata_from_request(request: dict) -> dict:
        metadata = dict()
        for column in request.get("schema").get("fields"):
            column_type = column.get("type")
            metadata[column.get("name")] = {
                "type": column_type
            }

        return metadata

    def _generate_cache_file_name(self) -> str:
        """
        Cache file name is created by encrypt the sql script into a MD5
        string, thus avoiding duplicated names.
        """

        file_name = self.connection_alias + self.query
        hashed_file_name = md5(file_name.encode())
        return str(hashed_file_name.hexdigest()) + ".rds"

    def close_connection(self):
        # Since Big Query uses API to get data, no close_connection method is needed
        pass

    def _save_data(self, result_file_name: str = None) -> None:

        bq_client = self.connect()
        self._extract_data(bq_client)

    def _extract_data(self, bq_client) -> None:

        bq_response = bq_client._connection.api_request(
            "POST",
            f"/projects/{bq_client.project}/queries",
            data={"query": self.query, "useLegacySql": False}
        )

        job_complete = bq_response.get("jobComplete", False)
        job_id = bq_response.get("jobReference", {}).get("jobId")
        page_token = bq_response.get("pageToken")
        if not job_complete:
            bq_response = self._wait_for_job_to_complete(bq_client, job_id)

        retrieved_data = self._build_dataframe_from_response(bq_response)
        retrieved_data.to_csv(self.extracted_data_file_path, sep=';', encoding='utf-8', index=False)

        while page_token is not None:
            page_response = self._get_response_by_job_id(bq_client, job_id, {"pageToken": page_token})
            page_token = page_response.get("pageToken")

            # Append current page data to the previous one
            page_data = self._build_dataframe_from_response(page_response)
            page_data.to_csv(self.extracted_data_file_path, sep=';', encoding='utf-8',
                             mode='a', index=False, header=False)

            del page_data

    def _set_result_sql_file_path(self, result_file_name: str = None):

        if not result_file_name:
            file_name = self.connection_alias + self.query + str(uuid4())
            result_file_name = str(md5(file_name.encode()).hexdigest()) + ".csv"

        self.extracted_data_file_path = GlobalCalling.looq.temp_file(result_file_name, add_hash=False)
