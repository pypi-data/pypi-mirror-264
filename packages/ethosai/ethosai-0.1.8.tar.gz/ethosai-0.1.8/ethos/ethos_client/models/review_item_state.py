from enum import Enum


class ReviewItemState(str, Enum):
    APPROVED = "approved"
    COMMENTED = "commented"
    FLAGGED = "flagged"
    INITIALIZED = "initialized"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
