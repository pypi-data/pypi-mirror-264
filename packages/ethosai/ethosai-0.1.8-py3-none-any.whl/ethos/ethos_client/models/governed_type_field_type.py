from enum import Enum


class GovernedTypeFieldType(str, Enum):
    BASE_METADATA_FIELD = "base_metadata_field"
    OBJECT_FIELD = "object_field"
    VERSION_METADATA_FIELD = "version_metadata_field"

    def __str__(self) -> str:
        return str(self.value)
