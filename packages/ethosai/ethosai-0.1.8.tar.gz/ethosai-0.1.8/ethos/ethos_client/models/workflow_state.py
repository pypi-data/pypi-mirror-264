from enum import Enum


class WorkflowState(str, Enum):
    DONE = "done"
    FAILED = "failed"
    INITIALIZED = "initialized"
    IN_PROGRESS = "in_progress"

    def __str__(self) -> str:
        return str(self.value)
