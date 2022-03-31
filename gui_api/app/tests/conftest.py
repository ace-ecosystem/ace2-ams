import pytest

from fastapi.testclient import TestClient

from main import app


@pytest.fixture()
def client():
    """
    This fixture supplies a TestClient to use for testing API endpoints.
    """

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def client_valid_access_token(client, monkeypatch):
    """
    This fixture is the "client" fixture with a patched validate_access_token function so that it always validates.
    """

    def mock_validate_access_token():
        return {"sub": "analyst"}

    # Due to how imports work, patching __code__ accounts for all cases for how the function is imported and used.
    monkeypatch.setattr("core.auth.validate_access_token.__code__", mock_validate_access_token.__code__)

    yield client
