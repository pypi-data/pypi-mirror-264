from enum import Enum


class TaskState(str, Enum):
    DONE = "done"
    FAILED = "failed"
    INITIALIZED = "initialized"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    SKIPPED = "skipped"
    WAITING_ON_DEPENDENCIES = "waiting_on_dependencies"

    def __str__(self) -> str:
        return str(self.value)
