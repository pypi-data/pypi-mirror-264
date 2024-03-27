import pytest
import ethos
import os
from dotenv import load_dotenv
import vcr as vcrpy
import os


# Load environment variables from secrets.env
load_dotenv("secrets.env")
NAMESPACE_ID = os.getenv("NAMESPACE_ID", "fake-namespace-id")
PROJECT_ID = os.getenv("PROJECT_ID", "fake-project-id")
ETHOS_API_KEY = os.getenv("ETHOS_API_KEY", "fake-api-key")

ethos.config.api_key = ETHOS_API_KEY
ethos.config.namespace_id = NAMESPACE_ID
ethos.config.api_host = "http://localhost:9090"


@pytest.fixture
def vcr():
    record_mode = vcrpy.mode.NEW_EPISODES if os.getenv("RECORD", None) else vcrpy.mode.NONE
    return vcrpy.VCR(
        serializer="json",
        cassette_library_dir="tests/fixtures/cassettes",
        record_mode=record_mode,
        # Loosen the matching to allow for variable URIs. This will
        # make the cassettes return in order of the requests made.
        match_on=["method"],
        filter_headers=["Authorization"],
        decode_compressed_response=True,
    )
