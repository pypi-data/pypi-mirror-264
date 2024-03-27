from enum import Enum


class GovernedObjectMetadataType(str, Enum):
    BASE_METADATA = "base_metadata"
    VERSION_METADATA = "version_metadata"

    def __str__(self) -> str:
        return str(self.value)
