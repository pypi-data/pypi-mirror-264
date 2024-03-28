from typing import Optional
from inspect import ismethod

from looqbox.database.query_metrics import QueryMetric


class QueryLog:
    connection: str = ""
    query: str = ""
    time: str = ""
    mode: str = ""
    success: bool = False
    cached: Optional[bool] = None
    metrics: Optional[QueryMetric] = None

    def __init__(self, connection=None, query=None, time=None, mode="single", success=False, cached=False,
                 metrics=None):
        self.connection: str = connection
        self.query: str = query
        self.time: str = time
        self.mode: str = mode
        self.success: bool = success
        self.cached: Optional[bool] = cached
        self.metrics: Optional[QueryMetric] = metrics

    def _get_attributes_names(self):
        cls_attributes_names = []
        members = dir(self)
        for attribute in members:
            if not attribute.startswith('_'):
                if not ismethod(self.__getattribute__(attribute)):
                    cls_attributes_names.append(attribute)
        return cls_attributes_names

    def to_dict(self):
        attributes_names = self._get_attributes_names()
        attributes = {}
        for attribute in attributes_names:
            attributes[attribute] = self.__getattribute__(attribute)
        return attributes

    def __str__(self):
        return str(self.to_dict)
