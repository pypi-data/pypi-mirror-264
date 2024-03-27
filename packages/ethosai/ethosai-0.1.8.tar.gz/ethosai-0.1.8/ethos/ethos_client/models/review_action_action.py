from enum import Enum


class ReviewActionAction(str, Enum):
    APPROVE = "approve"
    COMMENT = "comment"
    FLAG = "flag"

    def __str__(self) -> str:
        return str(self.value)
