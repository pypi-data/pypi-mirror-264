import concurrent.futures
import datetime
import re
from platform import system
from typing import Callable

from looqbox.database.database_exceptions import TimeOutException
from looqbox.database.query_setting import QuerySettings
from looqbox.global_calling import GlobalCalling
from looqbox.objects.visual.looq_table import ObjTable


class SqlThreadManager:

    def __init__(self):
        self.timeout_settings = {"Windows": None}
        self.test_mode = GlobalCalling.looq.test_mode
        self.id_pattern = "(?<=[/])\\d+"
        self.start_time = 0
        self._method: Callable = None

    def set_to_query_mode(self):
        self._method = self._sql_thread

    def set_to_extract_mode(self):
        self._method = self._extract_thread

    def parallel_execute(self, queries_list: list[QuerySettings]|list[dict], number_of_threads=1):
        self._check_batch_queries(queries_list)

        timer = self._get_timeout_methods()

        if self._any_query_is_dict(queries_list):
            queries_list = [QuerySettings.from_dict(query) for query in queries_list]

        response_timeout = self._get_response_timeout()
        #timer.set_timeout(response_timeout)
        results = []

        self.start_time = datetime.datetime.now()
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
                queries_results = [executor.submit(self._method, sql_item) for sql_item in queries_list]
            results.extend([query.result() for query in queries_results])
            executor.shutdown(wait=False, cancel_futures=True)

        except TimeOutException as ex:
            [sql_item["connection"].close() for sql_item in queries_list]
            total_sql_time = datetime.datetime.now() - self.start_time
            GlobalCalling.log_query(self.build_log(time=str(total_sql_time),
                                                   success=False,
                                                   mode="parallel")
                                    )

        except:
            exceptions = [query.exception() for query in queries_results if query.exception() is not None]
            raise Exception(exceptions)

        finally:
            timer.reset_timeout()
            if not self.test_mode:
                total_sql_time = datetime.datetime.now() - self.start_time
                self._update_response_timeout(total_sql_time)
        return results

    def _get_timeout_methods(self):
        import os
        from looqbox.utils.utils import open_file
        import json
        from looqbox.class_loader.class_loader import ClassLoader

        timeout_configuration_file = open_file(os.path.dirname(__file__), "..", "..", "resources",
                                               "timeout_settings_class_path.json")

        timeout_factory = json.load(timeout_configuration_file)

        class_path, class_name = timeout_factory[system().lower()].rsplit(".", 1)
        timer = ClassLoader(class_name, class_path).load_class()

        return timer

    def _any_query_is_dict(self, queries_list) -> bool:
        return any([isinstance(query, dict) for query in queries_list])

    def _check_batch_queries(self, queries_list):
        if queries_list is None or len(queries_list) == 0:
            raise Exception("No query is currently set to be executed")

    def _sql_thread(self, sql_item):
        from looqbox.database.database_functions import connect

        sql_item.connection = connect(sql_item.connection)

        table = ObjTable()

        sql_item.connection.set_query_script(sql_item.query)

        if sql_item.cache_time is not None:
            sql_item.connection.use_query_cache(sql_item.cache_time,
                                                       self.start_time, query_mode="parallel")
        else:
            # The protected method _call_query_executor is used to
            # take advantage o the DB error handling and the timeout
            # exception is managed by the parallel_execute method.

            sql_item.connection._call_query_executor(self.start_time, query_mode="parallel")

        table.data = sql_item.connection.retrieved_data

        table.rows = table.data.shape[0]
        table.cols = table.data.shape[1]

        #thread_log.info("Finishing" + str(sql_item.get('query')))

        return table

    def _extract_thread(self, sql_item):
        from looqbox.database.database_functions import connect

        method = "query_caller" if sql_item.use_query_caller else "default"
        sql_item.connection = connect(sql_item.connection, query_method=method)

        sql_item.connection.set_query_script(sql_item.query)
        result_file_link  = sql_item.connection._call_sql_extractor(sql_item.result_file_name, query_mode="parallel")

        return result_file_link

    def create_log_file(self):
        import logging

        log_format = "%(threadName)s: %(asctime)s: %(message)s"
        logging.basicConfig(format=log_format,
                            level=logging.INFO,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=GlobalCalling.looq.temp_file(self._get_script_id() + 'parallel.log',
                                                                  add_hash=False)
                            )
        return logging

    def _get_response_timeout(self) -> int:
        timeout = int(GlobalCalling.looq.response_timeout) if not self.test_mode else 0
        return timeout

    def _update_response_timeout(self, consumed_time: datetime.timedelta) -> None:
        GlobalCalling.looq.response_timeout -= int(round(consumed_time.total_seconds(), 0))

    def _get_script_id(self):

        if not self.test_mode:
            script_id = str(re.findall(self.id_pattern, GlobalCalling.looq.response_dir())[0]) + "-"
        else:
            script_id = ""
        return script_id
