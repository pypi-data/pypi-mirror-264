from enum import Enum


class ProxyInferencePredictionMethodType0(str, Enum):
    BIFSG = "BIFSG"
    BISG = "BISG"
    GEOCODE_ONLY = "GEOCODE_ONLY"

    def __str__(self) -> str:
        return str(self.value)
