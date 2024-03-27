from enum import Enum


class ReviewItemStateReason(str, Enum):
    INITIALIZED = "initialized"
    USER_APPROVED = "user_approved"
    USER_COMMENTED = "user_commented"
    USER_FLAGGED = "user_flagged"
    USER_REJECTED = "user_rejected"

    def __str__(self) -> str:
        return str(self.value)
