from enum import Enum


class GovernedTypeFieldCreateDatatype(str, Enum):
    BOOLEAN = "boolean"
    FLOAT = "float"
    INTEGER = "integer"
    JSON = "json"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
