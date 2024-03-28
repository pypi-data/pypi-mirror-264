from dataclasses import dataclass
from typing import List, Optional
from looqbox.database.connections.connection_base import BaseConnection


QUERY_REQUIRED_KEYS = ["connection", "query"]

@dataclass
class QuerySettings:
    connection: BaseConnection
    query: str
    replace_parameters: Optional[List[str]]
    close_connection: Optional[bool]
    show_query: Optional[bool]
    null_as: Optional[str]
    add_quotes: Optional[bool]
    cache_time: Optional[int]
    result_file_name: Optional[str]
    use_query_caller: Optional[bool]

    @staticmethod
    def from_dict(query_as_dict:dict):

        if isinstance(query_as_dict, QuerySettings):
            return query_as_dict

        _is_connections_valid(query_as_dict)

        return QuerySettings(
        connection = query_as_dict.get("connection"),
        query = query_as_dict.get("query"),
        replace_parameters = query_as_dict.get("replace_parameters"),
        close_connection = query_as_dict.get("close_connection", True),
        show_query = query_as_dict.get("show_query", False),
        null_as = query_as_dict.get("null_as", "-"),
        add_quotes = query_as_dict.get("add_quotes", False),
        cache_time = query_as_dict.get("cache_time"),
        result_file_name = query_as_dict.get("result_file_name"),
        use_query_caller = query_as_dict.get("use_query_caller", False)
        )

def _is_connections_valid(sql_item: dict) -> None:
    if not _have_required_keys(sql_item):
        raise ValueError(f'Missing required keys. All queries must have the fields: {QUERY_REQUIRED_KEYS}')

def _have_required_keys(sql_item: dict) -> bool:
    if all([req_key in sql_item.keys() for req_key in QUERY_REQUIRED_KEYS]):
        return True
    else:
        return False