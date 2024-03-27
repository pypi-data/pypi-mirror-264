from enum import Enum


class DatasetSchemaColumnErrorType0(str, Enum):
    DTYPE_CONFLICT = "dtype_conflict"
    TYPE_CONFLICT_NOT_UNIQUE = "type_conflict_not_unique"
    TYPE_NOT_ALLOWED = "type_not_allowed"

    def __str__(self) -> str:
        return str(self.value)
