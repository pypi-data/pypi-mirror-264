import uuid
from typing import Dict, Optional, Any

from looqbox.integration.user import User
import os
import re
import string
import random

from looqbox.utils.singleton import Singleton


def random_hash(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for pos in range(size))


class Looqbox(metaclass=Singleton):

    def __init__(self, home=None, version=None, language=None, looqbox_path=None, response_path=None, jdbc_path=None,
                 config_path=None, temp_dir=None, config_file=None, client_file=None, connection_file=None,
                 connection_config=None, driver_path=None, client_key=None, client_host=None, test_mode=True,
                 publish_test=None, query_list=None, entity_sync_path=None, response_timeout=None, date_format=None,
                 decimal_separator=None):
        self.home = home
        self.version = version
        self.language = language
        self.looqbox_path = looqbox_path
        self.response_path = response_path
        self.entity_sync_path = entity_sync_path
        self.jdbc_path = jdbc_path
        self.driver_path = driver_path
        self.config_path = config_path
        self.client_key = client_key
        self.client_host = client_host
        self.client_file = client_file
        self.config_file = config_file
        self.connection_file = connection_file
        self.connection_config = connection_config
        self.temp_dir = temp_dir
        self.test_mode = test_mode
        self.publish_test = publish_test
        self.user = User()
        self.response_timeout = response_timeout if response_timeout is not None else 30  # set a default value if Java fail to pass parameter
        self.decimal_separator = decimal_separator if decimal_separator is not None else self.set_default_decimal_separator()
        self.date_format = date_format if date_format is not None else self._set_default_date_format()
        self.datetime_format = date_format if date_format is not None else self._set_default_datetime_format()
        self.feature_flags = None
        self.domains = None
        self.question = None
        self.session_id = ""
        self.query_list = query_list or {}
        self.response_parameters = None
        self.response_filters = None
        self.response_partitions = None
        self.response_keywords: Optional[Dict[str, Any]] = None
        self.syntax_tree = None

    def set_default_decimal_separator(self):

        separator_options = {"en-us": ".",
                             "pt-br": ","}

        separator = separator_options.get(self.language, ",")

        return separator

    def _set_default_date_format(self):

        date_options = {"en-us": "mm/dd/yyyy",
                        "pt-br": "dd/mm/yyy"}

        date_format = date_options.get(self.language, "dd/mm/yy")
        return date_format

    def _set_default_datetime_format(self):
        datetime_options = {"en-us": "mm/dd/yyyy hh:mm:ss",
                            "pt-br": "dd/mm/yyyy hh:mm:ss"}

        datetime_format = datetime_options.get(self.language, "dd/mm/yy hh:mm:ss")
        return datetime_format

    def response_dir(self, *args):

        if self.response_path is not None:
            resp_path = os.path.dirname(self.response_path)
        else:
            resp_path = os.getcwd()

        return os.path.join(resp_path, *args)

    def temp_file(self, file_name=None, temporary_dir="tmp", add_hash=True):

        if self.temp_dir is not None:
            temporary_dir = self.temp_dir

        if file_name is None:
            file_name = "file__h" + random_hash(15) + "h__.tmp"
        elif add_hash:
            base_name = re.sub('\.(.+)', '', file_name)
            extension_name = re.search('\.(.+)', file_name).group(0)
            file_name = base_name + "__h" + random_hash(15) + "h__" + extension_name

        return os.path.join(temporary_dir, file_name)
