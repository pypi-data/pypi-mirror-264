import datetime
import os

import pandas as pd

from looqbox.database.connections.connection_base import BaseConnection
from looqbox.global_calling import GlobalCalling


class QueryCallerJDBCConnection(BaseConnection):

    def __init__(self, connection_name: str, parameter_as_json=False, use_all_jars=False):
        super().__init__()
        self.connection_alias = connection_name
        self.parameter_as_json = parameter_as_json
        self.import_all_jars_files = use_all_jars

        self.JAVA_PATH = ""
        self.result_file = None

    def _get_query_executor_jar_path(self) -> str:
        self._set_java_path()
        return os.path.join(os.path.dirname(__file__), "jars", "QueryCaller.jar")

    def set_query_script(self, sql_script: str) -> None:
        self.query = sql_script

    def connect(self) -> None:

        self.credential = self._get_connection_credentials(self.connection_alias)

    def _set_java_path(self) -> None:
        self.JAVA_PATH = os.environ.get("JAVA_HOME", "/usr/bin/java")

    def _get_all_jar_files(self) -> list:
        """
        Get and append all jar files required for each entry in connection.json
        """

        jar_list = list()
        file_connections = self._get_connection_file()

        # get the jar files for each connection
        for connections in file_connections:

            # Avoid errors due some wrong connection register
            try:
                connection_jar = self._get_connection_credentials(connections)["jar"]
            except:
                connection_jar = []

            jar_list.extend(connection_jar)
        return jar_list

    def _get_connection_credentials(self, connection: str) -> dict:
        """
        Get credentials for a list of connections.

        :param connection: String or list of database names
        :return: A Connection object
        """
        driver_path = []
        connection_credential = self._get_connection_file()

        try:
            if not self.parameter_as_json:
                connection_credential = GlobalCalling.looq.connection_config[connection]
            else:
                connection_credential = connection_credential[connection]
        except KeyError:
            raise Exception(
                "Connection " + connection + " not found in the file " + GlobalCalling.looq.connection_file)

        if self._connection_have_driver(connection_credential):
            driver_path = self._get_drivers_path(connection_credential, driver_path)
        connection_credential["jar"] = driver_path
        return connection_credential

    def _connection_have_driver(self, connection) -> bool:
        return connection.get('driverFile') is not None

    def _get_drivers_path(self, connection_credential, driver_path) -> str:

        import os

        conn_file_name, conn_file_extension = os.path.splitext(connection_credential['driverFile'])
        old_driver_folder_path = os.path.join(GlobalCalling.looq.jdbc_path + '/' + conn_file_name + conn_file_extension)
        new_driver_folder_path = os.path.join(GlobalCalling.looq.jdbc_path + '/' + conn_file_name)
        if new_driver_folder_path:
            for file in os.listdir(new_driver_folder_path):
                if self._is_jar(file):
                    driver_path.append(new_driver_folder_path + '/' + file)

        elif old_driver_folder_path:
            driver_path = old_driver_folder_path
        return driver_path

    def _is_jar(self, file: str) -> bool:
        return not file.startswith('.') and '.jar' in file

    def _call_query_executor(self, start_time, query_mode="single"):

        import os

        try:
            self._build_query_settings_file()
            self._start_external_process()
            self._get_query_result()
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=True,
                                                   mode=query_mode)
                                    )

            self._update_response_timeout(total_sql_time)
        except:

            error_message = self._get_error_message_from_java()
            if os.path.isfile(self.result_file + ".txt"):
                os.remove(self.result_file + ".txt")

            total_sql_time = datetime.datetime.now() - start_time

            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=False,
                                                   mode=query_mode))

            raise Exception(error_message)

        finally:
            os.remove(self.setting_file)

    def _get_result_file_name(self):
        from hashlib import md5
        from uuid import uuid4

        result_file_name = self.connection_alias + self.query + str(uuid4())
        digested_name = str(md5(result_file_name.encode()).hexdigest())
        return digested_name

    def _build_query_settings_file(self):

        from looqbox.json_encoder import JsonEncoder
        import json

        result_file_name = self._get_result_file_name()
        self.result_file = GlobalCalling.looq.temp_file(result_file_name, add_hash=False)

        query_settings = {
            "connectionName": self.connection_alias,
            "query": self.query,
            "responseTimeout": self._get_response_timeout(),
            "resultFilePath": self.result_file,
            "jarPath": self.credential["jar"][0],
            "connectionCredentials": {"connString": self.credential.get("connString"),
                                      "driver": self.credential.get("driver"),
                                      "user": self.credential.get("user"),
                                      "pass": self.credential.get("pass")
                                      }
        }

        self.setting_file = GlobalCalling.looq.temp_file(result_file_name + ".json", add_hash=False)

        json_content = json.dumps(query_settings, indent=1, allow_nan=True, cls=JsonEncoder)
        with open(self.setting_file, "w") as query_settings:
            query_settings.write(json_content)
            query_settings.close()

    def _start_external_process(self) -> None:
        """
        Function to get the table resulting from the query
        """

        import subprocess
        QUERY_EXECUTOR = self._get_query_executor_jar_path()

        subprocess.call([self.JAVA_PATH, '-jar', QUERY_EXECUTOR, self.setting_file])

    def _get_query_result(self) -> None:

        self.retrieved_data = pd.read_csv(f"{self.result_file}.csv")
        self.query_metadata = {}#metadata

    def _get_error_message_from_java(self) -> str:

        error_file = open(self.result_file + ".txt", "r")

        error_message = error_file.read()
        error_file.close()
        return error_message

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
            'INTEGER': ('BOOLEAN', 'BIGINT', 'BIT', 'INTEGER', 'SMALLINT', 'TINYINT'),
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

    def _save_data(self):
        try:
            self._build_query_settings_file()
            self._start_external_process()
            if os.path.isfile(f"{self.result_file}.csv"):
                self._update_file_name()
                if f"{self.result_file}.csv" != self.extracted_data_file_path:
                    self._rename_result_sql_file()

        except:
            error_message = self._get_error_message_from_java()
            raise Exception(error_message)

    def _update_file_name(self) -> None:
        """
        Given that self.result_success_file_name is defined after the _set_result_sql_file_path method was called
        in the super class, it's essential to update the name for the extracted file.
        """
        if self.extracted_data_file_path is None and self.result_file is not None:
            self.extracted_data_file_path = f"{self.result_file}.csv"

    def _set_result_sql_file_path(self, result_file_name: str = None) -> None:
        if not result_file_name:
             self._update_file_name()
        else:
            self.extracted_data_file_path =  GlobalCalling.looq.temp_file(result_file_name, add_hash=False)

    def _rename_result_sql_file(self):
        os.rename(f"{self.result_file}.csv", self.extracted_data_file_path)