import pytest
import random

from tonic import Tonic
from tonic.classes import *
from tonic.exceptions import *
from tests.config import Config

@pytest.fixture
def tonic():
    config_data = Config.get()["testing"]
    tonic = Tonic(endpoint=config_data["api_endpoint"], access_id=config_data["auth_token_id"], secret_key=config_data["auth_token_secret"])
    return tonic

def test_status(tonic):
    # get status
    res = tonic.client_response(
        method="GET",
        url="/status?node_only=true"
        )
    assert res["status_code"] == 200