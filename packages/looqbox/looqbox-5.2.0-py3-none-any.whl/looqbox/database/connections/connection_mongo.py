import datetime
import re

import pandas as pd
import pymongo

from looqbox.database.connections.connection_base import BaseConnection
from looqbox.global_calling import GlobalCalling
from hashlib import md5
from uuid import uuid4



class MongoConnection(BaseConnection):
    def __init__(self, connection_name: str,  **additional_args):
        super().__init__()
        self.connection_alias = connection_name
        self.connection_object = pymongo.mongo_client
        self.response_timeout = GlobalCalling.looq.response_timeout if not self.test_mode else 0

        self.database_name_pattern = "(?<=\\w/)\\w+(?=[/\\w+]?)"

    def set_query_script(self, sql_script: dict) -> None:
        self.query = sql_script

    def connect(self):
        connection_credentials = self._get_connection_credentials(self.connection_alias)
        self.connection_object = self._open_mongo_connection(connection_credentials)

    def _open_mongo_connection(self, connection_credential: dict) -> pymongo.mongo_client:
        # Since the original object MongoClient, it's the one that has the close connection method,
        # it must be passed forward, until the very end of sql_execute
        self.database = self._get_database_from_mongo_connString(connection_credential.get("connString"))
        mongo_connection = pymongo.MongoClient(connection_credential.get("connString"))
        return mongo_connection

    def _get_database_from_mongo_connString(self, connection_string: str) -> str:
        database_name = re.findall(self.database_name_pattern, connection_string)[0]
        return database_name

    def set_database_name_pattern(self, pattern: str) -> None:
        self.database_name_pattern = pattern

    def _get_connection_credentials(self, connection: str, parameter_as_json=False) -> dict:
        """
        Get credentials for a list of connections.

        :param connection: String or list of database names
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
            query_result: pymongo.cursor = self._get_query_result()
            self.retrieved_data = pd.DataFrame(query_result)
            self.query_metadata = dict(self.retrieved_data.dtypes)
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=True,
                                                   mode=query_mode)
                                    )
            self._update_response_timeout(total_sql_time)

        except Exception as execution_error:

            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=False,
                                                   mode=query_mode))
            raise execution_error

    def _get_query_result(self):
        database_connection = self.connection_object[self.database]
        collection = database_connection[(self.query.get("collection"))]
        query_result = collection.find(self.query.get("query"), self.query.get("fields"))
        return query_result


    def _generate_cache_file_name(self) -> str:
        """
        Cache file name is created by encrypt the sql script into a MD5
        string, thus avoiding duplicated names.
        """
        
        file_name = self.connection_alias + self._convert_query_to_string()
        hashed_file_name = md5(file_name.encode())
        return str(hashed_file_name.hexdigest()) + ".rds"

    def _convert_query_to_string(self) -> str:
        query_as_string = ""
        keys = list(self.query.keys())
        values = list(self.query.values())
        for i in range(len(keys)):
            query_as_string += str(keys[i]) + " " + str(values[i]) + ";"
            query_as_string += " "

        # Removed addition blank space at the end
        query_as_string = query_as_string[:-1]

        # since the character { and } could mess up the md5 conversion between R and Python
        # theses must be removed from the string
        query_as_string = query_as_string.replace("{", "").replace("}", "")
        return query_as_string

    def close_connection(self):
        self.connection_object.close()

    def _save_data(self, result_file_name: str = None):

        query_result = self._get_query_result()
        self._save_cursor_to_csv(query_result)

    def _save_cursor_to_csv(self, query_data: pymongo.cursor):

        self._create_exported_file(query_data[0])
        self._add_rows_to_exported_file(query_data[1:])

    def _create_exported_file(self, first_row:dict) -> None:

        first_row_data = pd.DataFrame(first_row, index=[0])
        first_row_data.to_csv(self.extracted_data_file_path, sep=';', encoding='utf-8', index=False)
        del first_row_data

    def _add_rows_to_exported_file(self, query_data: pymongo.cursor) -> None:

        accumulated_rows = list()

        for row in query_data:
            accumulated_rows.append(row)
            if len(accumulated_rows) == self.insert_rows_limit:
                rows_data = pd.DataFrame(accumulated_rows)
                rows_data.to_csv(self.extracted_data_file_path, sep=';', encoding='utf-8',
                                     mode='a', index=False, header=False)
                del rows_data
                accumulated_rows.clear()

        if len(accumulated_rows) > 0:
            try:
                rows_data = pd.DataFrame(accumulated_rows, index=[0])
            except ValueError:
                rows_data = pd.DataFrame(accumulated_rows)
            rows_data.to_csv(self.extracted_data_file_path, sep=';', encoding='utf-8',
                             mode='a', index=False, header=False)

            del rows_data
            accumulated_rows.clear()

    def _set_result_sql_file_path(self, result_file_name: str = None):

        if not result_file_name:
            file_name = self.connection_alias + self._convert_query_to_string() + str(uuid4())
            result_file_name = str(md5(file_name.encode()).hexdigest()) + ".csv"

        self.extracted_data_file_path = GlobalCalling.looq.temp_file(result_file_name, add_hash=False)
