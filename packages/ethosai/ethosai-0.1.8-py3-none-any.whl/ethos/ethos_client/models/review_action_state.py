from enum import Enum


class ReviewActionState(str, Enum):
    DRAFT = "draft"
    PROCESSED = "processed"

    def __str__(self) -> str:
        return str(self.value)
