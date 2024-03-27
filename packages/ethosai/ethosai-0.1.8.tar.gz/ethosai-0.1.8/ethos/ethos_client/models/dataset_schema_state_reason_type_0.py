from enum import Enum


class DatasetSchemaStateReasonType0(str, Enum):
    COLUMN_ERROR = "column_error"
    LOAD_ERROR = "load_error"
    NO_ACTUAL_VALUES_COLUMN = "no_actual_values_column"
    NO_ID_COLUMN = "no_id_column"
    NO_PREDICT_OR_PREDICT_PROBA_COLUMN = "no_predict_or_predict_proba_column"
    NO_TARGET_COLUMN = "no_target_column"

    def __str__(self) -> str:
        return str(self.value)
