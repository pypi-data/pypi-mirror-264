from enum import Enum


class ResourceCreateType(str, Enum):
    BOOLEAN = "boolean"
    DATASET = "dataset"
    DATETIME = "datetime"
    FILE = "file"
    FILE_SET = "file_set"
    FLOAT = "float"
    FLOAT_SERIES = "float_series"
    INTEGER = "integer"
    STRING = "string"
    STRING_SERIES = "string_series"
    STRING_SET = "string_set"

    def __str__(self) -> str:
        return str(self.value)
