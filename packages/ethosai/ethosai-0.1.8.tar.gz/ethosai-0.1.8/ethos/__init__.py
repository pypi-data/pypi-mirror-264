from .ethos_objects import *


def init_model(*, namespace_id: str, model_name: str, **kwargs) -> Model:
    return Model(namespace_id=namespace_id, name=model_name, **kwargs)


# Use ethos.config to access the global config object.
config = Config()
