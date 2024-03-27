from enum import Enum


class DatasetSchemaState(str, Enum):
    ERROR = "error"
    INITIALIZED = "initialized"
    PROCESSED = "processed"

    def __str__(self) -> str:
        return str(self.value)
