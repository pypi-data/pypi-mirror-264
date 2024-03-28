import datetime
import json
import os
from abc import ABC, abstractmethod
from platform import system
from sys import getsizeof

from multimethod import multimethod
from pandas import DataFrame

from looqbox.class_loader.class_loader import ClassLoader
from looqbox.database.database_exceptions import TimeOutException
from looqbox.database.query_log import QueryLog
from looqbox.database.query_metrics import QueryMetric
from looqbox.global_calling import GlobalCalling
from looqbox.utils.utils import open_file


class BaseConnection(ABC):

    def __init__(self):
        self.test_mode = GlobalCalling.looq.test_mode
        self.connection_alias = ""
        self.query = ""
        self.retrieved_data = DataFrame()
        self.query_metadata = dict()
        self.extracted_data_file_path = None
        self.is_optimized_for_large_dataset = False
        self.insert_rows_limit = 0  # define the batch size for csv export

        connection_configuration_file = open_file(
            os.path.dirname(__file__), "..", "..", "configuration", "database_connection_settings.json"
        )

        self.connection_configuration = json.load(connection_configuration_file)
        connection_configuration_file.close()

    def get_result_metrics(self):
        return QueryMetric(rows=self.retrieved_data.shape[0],
                           columns=self.retrieved_data.shape[1],
                           file_size_kb=round(getsizeof(self.retrieved_data) / 1024, 3))

    def build_log(self, time: str = "", success: bool = False, mode: str = "single", cached: bool = False):

        return QueryLog(connection=self.connection_alias,
                        query=self.query,
                        time=time,
                        success=success,
                        mode=mode,
                        cached=cached,
                        metrics=self.get_result_metrics().to_dict())

    def set_optimization_for_large_datasets(self, is_optimized: bool) -> None:
        self.is_optimized_for_large_dataset = is_optimized

    @staticmethod
    def _get_timeout_methods():

        timeout_configuration_file = open_file(os.path.dirname(__file__), "..", "..",
                                               "configuration", "timeout_settings_class_path.json")

        timeout_factory = json.load(timeout_configuration_file)

        class_path, class_name = timeout_factory[system().lower()].rsplit(".", 1)
        timer = ClassLoader(class_name, class_path).load_class()

        return timer

    @abstractmethod
    def set_query_script(self, sql_script):
        pass

    @abstractmethod
    def connect(self):
        pass

    def _get_response_timeout(self) -> int:
        if self.test_mode:
            return int(os.getenv("QUERY_TIME_LIMIT", 300))
        return int(GlobalCalling.looq.response_timeout or 300)

    @staticmethod
    def _update_response_timeout(consumed_time: datetime.timedelta) -> None:
        GlobalCalling.looq.response_timeout -= int(round(consumed_time.total_seconds(), 0))

    @multimethod
    def execute(self, cache_time: None) -> None:
        timer = self._get_timeout_methods()

        response_timeout = self._get_response_timeout()
        # timer.set_timeout(response_timeout)

        start_time = datetime.datetime.now()

        try:
            self._call_query_executor(start_time)
        except TimeOutException as ex:
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=False)
                                    )
            raise ex
        finally:
            self.close_connection()
            timer.reset_timeout()

    @multimethod
    def execute(self, cache_time: int) -> None:
        timer = self._get_timeout_methods()

        response_timeout = self._get_response_timeout()
        timer.set_timeout(response_timeout)
        start_time = datetime.datetime.now()
        try:
            self.use_query_cache(cache_time, start_time)
        except TimeOutException as ex:
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=False,
                                                   cached=True)
                                    )
            raise ex
        except FileNotFoundError as file_not_found_error:
            raise file_not_found_error
        except IOError as io_error:
            raise io_error
        finally:
            self.close_connection()
            timer.reset_timeout()

    @abstractmethod
    def _call_query_executor(self, query_timer, query_mode="single"):
        """
        Method that call _get_query_result implementing the try-except statement using the connection type
        specific error handlers
        """
        pass

    @abstractmethod
    def _get_query_result(self):
        """
        Method to execute the query properly without any try-except statements
        this model allow the execution of several queries in parallel
        """
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def _generate_cache_file_name(self):
        pass

    def use_query_cache(self, cache_time, start_time, query_mode="single"):
        # since cache is saved in rds format, it's necessary
        # to load the equivalent R functions

        # data frame name used in rds file, since R and Python shared the same files,
        # no name has to be attached to the data
        DF_NAME = None
        cache_name = self._generate_cache_file_name()

        if self.test_mode:
            self.check_if_temp_folder_exists()
        cache_file = GlobalCalling.looq.temp_file(cache_name, add_hash=False)

        if self._is_cache_still_valid(cache_file, cache_time):
            self._get_cached_data(DF_NAME, cache_file, start_time, query_mode)
        else:
            self._create_new_cache_file(cache_file, start_time, query_mode)

    def _create_new_cache_file(self, cache_file: str, start_time, query_mode) -> None:
        from pyreadr import write_rds

        self._call_query_executor(start_time, query_mode)

        if self.retrieved_data.empty:
            return None

        if self.test_mode:
            print("creating cache\npath:", cache_file)

        try:
            write_rds(cache_file, self.retrieved_data)
        except Exception as error:
            raise error

    def _get_cached_data(self, DF_NAME: None, cache_file: str, start_time, query_mode="single") -> None:
        from pyreadr import read_r

        if self.test_mode:
            print("using cache\npath:", cache_file)
        try:
            cached_data = read_r(cache_file)[DF_NAME]
            self.retrieved_data = DataFrame(cached_data, columns=cached_data.keys())
            self.query_metadata = {}  # temporally disable metadata for cache
            total_sql_time = datetime.datetime.now() - start_time

            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=True, mode=query_mode,
                                                   cached=True)
                                    )

        except FileNotFoundError as file_exception:
            raise file_exception

    @staticmethod
    def _get_connection_file() -> dict:
        import json
        try:
            if isinstance(GlobalCalling.looq.connection_config, dict):
                file_connections = GlobalCalling.looq.connection_config
            else:
                file_connections = open(GlobalCalling.looq.connection_config)
                file_connections = json.load(file_connections)
        except FileNotFoundError:
            raise Exception("File connections.json not found")
        return file_connections

    @staticmethod
    def _is_cache_still_valid(cache_file, cache_time) -> bool:
        import time
        return os.path.isfile(cache_file) and (time.time() - os.stat(cache_file).st_mtime) < cache_time

    @staticmethod
    def check_if_temp_folder_exists() -> None:
        temp_path = GlobalCalling.looq.temp_dir
        if not os.path.isdir(temp_path):
            os.mkdir(temp_path)

    def extract_data_to_file(self, result_file_name: str = None):

        result_file_path = self._call_sql_extractor(result_file_name)

        return result_file_path

    def _call_sql_extractor(self, result_file_name, query_mode="single"):

        start_time = datetime.datetime.now()
        try:

            self.insert_rows_limit = self.connection_configuration.get("exportBatchSizeLimit", 100)
            self._set_result_sql_file_path(result_file_name)
            self._save_data()
            total_sql_time = datetime.datetime.now() - start_time
            self.log_query(query_mode, total_sql_time, success=True)
            self._update_response_timeout(total_sql_time)

        except FileNotFoundError as file_not_found_error:
            total_sql_time = datetime.datetime.now() - start_time
            self.log_query(query_mode, total_sql_time, success=False)
            raise file_not_found_error

        except IOError as io_error:
            total_sql_time = datetime.datetime.now() - start_time
            self.log_query(query_mode, total_sql_time, success=False)
            raise io_error

        except Exception as general_error:
            total_sql_time = datetime.datetime.now() - start_time
            self.log_query(query_mode, total_sql_time, success=False)
            raise general_error

        finally:
            self.close_connection()

        return self.extracted_data_file_path

    def log_query(self, query_mode, total_sql_time, success=False):
        GlobalCalling.log_query(
            self.build_log(
                time=str(total_sql_time),
                success=success,
                mode=query_mode
            )
        )

    @abstractmethod
    def _save_data(self):
        pass

    @abstractmethod
    def _set_result_sql_file_path(self, result_file_name: str = None):
        pass

    @staticmethod
    def _get_metadata_from_dataframe(dataframe: DataFrame) -> dict:
        # Mapping pandas types to SQL types
        type_mapping = {
            'object': 'VARCHAR',
            'int64': 'INT',
            'int32': 'INT',
            'float64': 'FLOAT',
            'bool': 'BOOL',
            'datetime64[ns]': 'DATETIME',
            'datetime64[ns, UTC]': 'DATETIME'
        }

        # In our frontend, we expect the following types
        expected_types = {
            'INT': 'INTEGER',
            'VARCHAR': 'STRING'
        }

        # Get types of each column in the DataFrame
        df_types = dataframe.dtypes.apply(lambda x: type_mapping[str(x)])

        # Convert to supported types
        df_types = df_types.apply(lambda row_type: expected_types.get(row_type, row_type))

        # Return as dict with required format
        return {col: {'type': dtype} for col, dtype in df_types.items()}
