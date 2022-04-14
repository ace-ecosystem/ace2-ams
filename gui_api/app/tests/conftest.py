import pytest
import requests_mock as rm_module

from fastapi.testclient import TestClient

from core.auth import validate_access_token
from main import app


@pytest.fixture()
def client():
    """
    This fixture supplies a TestClient to use for testing API endpoints.
    """

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def client_valid_access_token(client):
    """
    This fixture is the "client" fixture with a patched validate_access_token function so that it always validates.
    """

    def mock_validate_access_token():
        return {"sub": "analyst"}

    app.dependency_overrides[validate_access_token] = mock_validate_access_token

    yield client

    app.dependency_overrides = {}


@pytest.fixture()
def requests_mock(request):
    m = rm_module.Mocker(real_http=True)
    m.start()
    request.addfinalizer(m.stop)
    return m
