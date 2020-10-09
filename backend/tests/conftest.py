
# project/tests/conftest.py


import os

import pytest
from starlette.testclient import TestClient

from app import main


@pytest.fixture(scope="module")
def test_app():
    # set up
    # main.app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(main.app) as test_client:
        # testing
        yield test_client

    # tear down