from enum import Enum


class GovernedTypeCreateObjectClassification(str, Enum):
    CUSTOM = "custom"
    MACHINE_LEARNING_MODEL = "machine_learning_model"

    def __str__(self) -> str:
        return str(self.value)
