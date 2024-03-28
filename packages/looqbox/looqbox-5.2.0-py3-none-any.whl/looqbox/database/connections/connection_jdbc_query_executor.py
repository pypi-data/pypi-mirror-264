import datetime
import json
import os
import warnings
from hashlib import md5
from os.path import exists
from time import sleep
from uuid import uuid4

import requests

from looqbox.database.database_exceptions import TimeOutException
from looqbox.database.connections.connection_base import BaseConnection
from looqbox.database.database_exceptions import TimeOutException
from looqbox.global_calling import GlobalCalling
from looqbox.json_encoder import JsonEncoder
from looqbox.utils.utils import open_file


class QueryExecutorJDBCConnection(BaseConnection):

    def __init__(self, connection_name: str, parameter_as_json=False, use_all_jars=False):

        super().__init__()
        self.connection_alias = connection_name
        self.result_success_file_name = None
        self.result_error_file_name = None
        self.result_metrics_file_name = None

        self.query_request = {"header": {}, "body": ""}
        self.query_endpoint = ""
        self.query_id = ""
        self.query_host = ""
        self.query_host_port = ""
        self.wait_time = 0
        self.request_status = "unknown"
        self.request_timeout = 0

    def set_query_script(self, sql_script: str) -> None:
        self.query = sql_script

    def _call_query_executor(self, start_time, query_mode="single"):

        try:
            self._get_query_result()
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query(
                self.build_log(
                    time=str(total_sql_time),
                    success=True,
                    mode=query_mode)
            )

            self._update_response_timeout(total_sql_time)
            # self._load_metrics_file() # temporally removed metrics file
        except TimeOutException as ex:
            raise ex
        except:
            error_message = self._get_error_message()

            total_sql_time = datetime.datetime.now() - start_time

            GlobalCalling.log_query(
                self.build_log(
                    time=str(total_sql_time),
                    success=False,
                    mode=query_mode)
            )
            raise Exception(error_message)

    def _get_error_message(self) -> str:

        try:
            error_message = self._start_file_watcher(self.result_error_file_name)
        except json.JSONDecodeError:
            raise Exception("An Error Had Occurred, but could not read error result file")

        return error_message

    def _load_metrics_file(self) -> dict:

        query_metrics = self._start_file_watcher(self.result_metrics_file_name)
        return query_metrics

    def _start_file_watcher(self, file_path: str):

        while True:
            sleep(self.wait_time)
            if exists(file_path):
                with open(file_path, "r") as file:
                    file_content = json.load(file)
                    file.close()
                break

        return file_content

    def connect(self) -> None:
        self._set_connection_configuration()

    def _set_connection_configuration(self) -> None:

        self.wait_time = self.connection_configuration.get("fileWatcherIntervalTime", 0)
        self.request_timeout = self.connection_configuration.get("requestTimeout", 5)

        self._set_query_host()
        self._set_query_host_port()
        self._set_query_endpoint()

    def _set_query_host(self):

        try:
            self.query_host = GlobalCalling.looq.domains["queryHost"]
        except:
            warnings.warn("Using local query host configuration")
            self.query_host = self.connection_configuration.get("queryHost", "http://localhost")

    def _set_query_host_port(self):

        try:
            self.query_host_port = GlobalCalling.looq.domains["queryHostPort"]
        except:
            warnings.warn("Using local query host port configuration")
            self.query_host_port = self.connection_configuration.get("queryHostPort", 8080)

    def _set_query_endpoint(self):

        try:
            self.query_endpoint = GlobalCalling.looq.domains["queryEndpoint"]
        except:
            warnings.warn("Using local query endpoint configuration")
            self.query_endpoint = self.connection_configuration.get("queryEndpoint", "query")

    def _get_query_result(self) -> None:
        self.build_request_body()
        try:
            self._post_query()
        except requests.RequestException as e:
            self._generate_request_error_file(self.request_status)
            raise e
        except:
            self._generate_request_error_file(self.request_status)
            raise Exception(f"Request Return With Status {self.request_status}")
        self.wait_for_query_result(datetime.datetime.now())
        self._load_query_retrieved_data()
        self.query_metadata = self._get_metadata_from_dataframe(self.retrieved_data)

    def build_request_body(self) -> None:

        from looqbox.json_encoder import JsonEncoder

        headers = {
            'Content-Type': 'application/json',
            'X-User-Id': str(GlobalCalling.looq.user.id)
        }

        body = json.dumps({"queries": [self._build_query_settings()]},
                          indent=1,
                          allow_nan=True,
                          cls=JsonEncoder
                          )

        self.query_request = {"header": headers, "body": body}

    def _build_query_settings(self) -> dict:

        self.result_success_file_name, \
            self.result_error_file_name, \
            self.result_metrics_file_name = self._get_results_file_name()

        query_settings = {
            "connectionId": self.connection_alias,
            "query": self.query,
            "timeout": self._get_response_timeout() * 1e3,  # should be set as milliseconds
            "responseDataFile": self.result_success_file_name,
            "responseErrorFile": self.result_error_file_name,
            "responseStatisticsFile": self.result_metrics_file_name
        }

        return query_settings

    def _get_results_file_name(self) -> tuple[str, str, str]:

        success_file_name = GlobalCalling.looq.temp_file(
            self._set_result_file_name(result_type="success") + ".csv", add_hash=False)

        error_file_name = GlobalCalling.looq.temp_file(
            self._set_result_file_name(result_type="error") + ".json", add_hash=False)

        metrics_file_name = GlobalCalling.looq.temp_file(
            self._set_result_file_name(result_type="metrics") + ".json", add_hash=False)

        return success_file_name, error_file_name, metrics_file_name

    def _set_result_file_name(self, result_type="") -> str:

        from hashlib import md5
        from uuid import uuid4

        result_file_name = str(uuid4()) + self.connection_alias + self.query + result_type
        digested_name = str(md5(result_file_name.encode()).hexdigest())
        return digested_name

    def _post_query(self) -> None:
        """
        Function to get the table resulting from the query
        """

        from requests import post

        query_service = self._get_query_service_host()
        query_request = post(
            query_service,
            headers=self.query_request.get("header"),
            data=self.query_request.get("body"),
            timeout=self.request_timeout
        )

        self.request_status = str(query_request.status_code)

        if query_request.status_code != 200:
            self._generate_request_error_file(self.request_status)

        # Temporally disable Query-Stop feature
        # post_content = json.loads(query_request.content)[0]
        # self.query_id = post_content.get("queryId", "")

    def _generate_request_error_file(self, status_code: str) -> None:

        status = {"message": f"Could Not Send Request.",
                  "requestCode": status_code,
                  "code": "internal"}

        json_content = json.dumps(status, indent=1, allow_nan=True, cls=JsonEncoder)
        with open(self.result_error_file_name, "w") as error_file:
            error_file.write(json_content)
            error_file.close()

    def _delete_query_job(self) -> None:

        from requests import delete

        delete_query_url = f"{self._get_query_service_host()}/{self.query_id}"
        delete(delete_query_url)

    def _get_query_service_host(self) -> str:

        query_service = f"{self.query_host}:{self.query_host_port}/{self.query_endpoint}"
        return query_service

    def wait_for_query_result(self, initial_time) -> None:

        while self.timeout_is_not_reached(initial_time):
            sleep(self.wait_time)
            if exists(self.result_success_file_name):
                self._load_query_retrieved_data()
                return
            elif exists(self.result_error_file_name):
                raise Exception("An Error Occurred While Executing The Query: ")
        raise TimeOutException("Timeout Has Been Reached")

    def timeout_is_not_reached(self, initial_time: datetime.timedelta) -> bool:

        is_valid = (datetime.datetime.now() - initial_time).seconds < self._get_response_timeout() \
            if not self.test_mode else True
        return is_valid

    def _load_query_retrieved_data(self) -> None:

        from pandas import read_csv
        self.retrieved_data = read_csv(self.result_success_file_name)

    def _generate_cache_file_name(self) -> str:
        """
        Cache file name is created by encrypt the sql script into a MD5
        string, thus avoiding duplicated names.
        """
        from hashlib import md5

        file_name = self.connection_alias + self.query
        hashed_file_name = md5(file_name.encode())
        return str(hashed_file_name.hexdigest()) + ".rds"

    def _filter_types(self, type_list: list) -> str:

        type_dict = {
            'CHAR': ('CHAR', 'NCHAR', 'NVARCHAR', 'VARCHAR', 'OTHER'),
            'LONGVARCHAR': ('CLOB', 'LONGVARCHAR', 'LONGNVARCHAR', 'NCLOB', 'SQLXML'),
            'BINARY': ('BINARY', 'BLOB', 'LONGVARBINARY', 'VARBINARY'),
            'INTEGER': ('BOOLEAN', 'BIGINT', 'BIT', 'INTEGER', 'SMALLINT', 'TINYINT', 'INT'),
            'FLOAT': ('FLOAT', 'REAL', 'DOUBLE'),
            'NUMERIC': ('DECIMAL', 'NUMERIC'),
            'DATE': ('DATE',),
            'TIME': ('TIME',),
            'TIMESTAMP': ('TIMESTAMP',),
            'ROWID': ('ROWID',)
        }
        column_type = None
        for db_type, aliases in type_dict.items():
            if type_list == aliases:
                column_type = db_type
        return column_type

    def close_connection(self) -> None:
        pass

    def _save_data(self) -> None:

        self.build_request_body()
        try:
            self._post_query()
        except requests.RequestException as e:
            self._generate_request_error_file(self.request_status)
            raise e
        except:
            self._generate_request_error_file(self.request_status)
            raise Exception(f"Request Return With Status {self.request_status}")

        self.wait_for_query_result(datetime.datetime.now())
        print(f"success file: {self.result_success_file_name}")
        self._update_file_name()
        if self.extracted_data_file_path != self.result_success_file_name:
            self._rename_result_sql_file()

    def _update_file_name(self) -> None:
        """
        Given that self.result_success_file_name is defined after the _set_result_sql_file_path method was called
        in the super class, it's essential to update the name for the extracted file.
        """
        if self.extracted_data_file_path is None and self.result_success_file_name is not None:
            self.extracted_data_file_path = self.result_success_file_name

    def _set_result_sql_file_path(self, result_file_name: str = None) -> None:
        if not result_file_name:
            self._update_file_name()
        else:
            self.extracted_data_file_path = GlobalCalling.looq.temp_file(result_file_name, add_hash=False)

    def _rename_result_sql_file(self) -> None:
        os.rename(self.result_success_file_name, self.extracted_data_file_path)
