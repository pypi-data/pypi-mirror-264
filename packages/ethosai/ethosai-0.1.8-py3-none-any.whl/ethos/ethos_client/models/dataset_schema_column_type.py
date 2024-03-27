from enum import Enum


class DatasetSchemaColumnType(str, Enum):
    ACTUAL_VALUES = "actual_values"
    DEFAULT = "default"
    ID = "id"
    PREDICT = "predict"
    PREDICT_PROBA = "predict_proba"
    PROTECTED = "protected"
    TARGET = "target"

    def __str__(self) -> str:
        return str(self.value)
