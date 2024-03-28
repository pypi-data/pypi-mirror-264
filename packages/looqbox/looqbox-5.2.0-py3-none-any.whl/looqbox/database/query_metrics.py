from inspect import ismethod



def to_camel_case(original_string):
    camel_string = "".join(char.capitalize() for char in original_string.lower().split("_"))
    return original_string[0].lower() + camel_string[1:]

class QueryMetric:
    rows: int = 0
    columns: int = 0
    file_size_kb: float  = 0.

    def __init__(self, rows:int =None, columns:int = None, file_size_kb:float = None):
        self.rows: int = rows
        self.columns: int = columns
        self.file_size_kb: float = file_size_kb

    def _get_attributes_names(self):
        cls_attributes_names = []
        members= dir(self)
        for attribute in members:
            if not attribute.startswith('_'):
                if not ismethod(self.__getattribute__(attribute)):
                    cls_attributes_names.append(attribute)
        return cls_attributes_names

    def to_dict(self):
        attributes_names = self._get_attributes_names()
        attributes = {}
        for attribute in attributes_names:
            attributes[to_camel_case(attribute)] = self.__getattribute__(attribute)
        return attributes

    def __dict__(self):
        return self.to_dict()

    def __str__(self):
        return str(self.to_dict())