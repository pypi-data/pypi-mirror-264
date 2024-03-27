import ethos
from ethos import ethos_objects
import pytest


@pytest.fixture
def model(request, vcr):
    namespace_id = ethos.config.namespace_id
    name = "HMDA-Q4-2024"
    with vcr.use_cassette(request.node.name):
        model = ethos_objects.Model(namespace_id=namespace_id, name=name)  # type: ignore
        # Initialize the model api call
        model._model

    return model


def test_model(model):
    assert model.namespace_id == ethos.config.namespace_id
    assert model.name == "HMDA-Q4-2024"
    assert model._model is not None


def test_model_new_version(request, vcr, model):
    with vcr.use_cassette(request.node.name):
        model_version = model.new_version()

    assert model_version.model == model._model
