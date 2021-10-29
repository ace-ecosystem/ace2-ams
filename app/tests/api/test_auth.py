import pytest
import time

from datetime import datetime, timedelta
from fastapi import status, testclient
from jose import jwt

from core.config import get_settings, Settings
from tests.helpers import create_test_user
from main import app


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "username,password",
    [
        ("johndoe", "wrongpassword"),
        ("wronguser", "abcd1234"),
    ],
)
def test_auth_invalid(client, db, username, password):
    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": username, "password": password})
    assert auth.status_code == status.HTTP_401_UNAUTHORIZED
    assert auth.json()["detail"] == "Invalid username or password"

    # Attempt to use a bogus token to access a protected API endpoint
    get = client.get("/api/user/", headers={"Authorization": "Bearer asdf"})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Invalid token"


def test_disabled_user(client, db):
    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    access_token = auth.json()["access_token"]
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["token_type"] == "bearer"
    assert access_token

    # Attempt to use the token to access a protected API endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    get = client.get("/api/user/", headers=headers)
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 1

    # Disable the user
    user_uuid = get.json()[0]["uuid"]
    update = client.patch(f"/api/user/{user_uuid}", headers=headers, json={"enabled": False})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # The user is disabled, but the token is still valid, so they will still have access until it expires.
    get = client.get("/api/user/", headers=headers)
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 1

    # However, they will not be able to authenticate again to receive a new token.
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    assert auth.status_code == status.HTTP_401_UNAUTHORIZED
    assert auth.json()["detail"] == "Invalid username or password"


def test_expired_token(client, db, monkeypatch):
    def mock_get_settings():
        settings = Settings()
        settings.jwt_access_expire_seconds = 1
        return settings

    # Patching __code__ works no matter how the function is imported
    monkeypatch.setattr("core.config.get_settings.__code__", mock_get_settings.__code__)

    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    access_token = auth.json()["access_token"]
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["token_type"] == "bearer"
    assert access_token

    # Attempt to use the token to access a protected API endpoint
    get = client.get("/api/user/", headers={"Authorization": f"Bearer {access_token}"})
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 1

    # Wait for the token to expire
    time.sleep(2)

    # Attempt to use the token to access a protected API endpoint now that the token is expired
    get = client.get("/api/user/", headers={"Authorization": f"Bearer {access_token}"})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Access token expired"


@pytest.mark.parametrize(
    "key",
    [
        ("username"),
        ("password"),
    ],
)
def test_missing_required_fields(client, key):
    create_json = {"username": "johndoe", "password": "abcd1234"}
    del create_json[key]
    create = client.post("/api/auth", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_missing_token(client):
    # Attempt to access a protected API endpoint without supplying an access token
    get = client.get("/api/user/")
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Not authenticated"


def test_wrong_token_type(client, db):
    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    refresh_token = auth.json()["refresh_token"]
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["token_type"] == "bearer"
    assert refresh_token

    # Attempt to use the refresh token to access a protected API endpoint
    get = client.get("/api/user/", headers={"Authorization": f"Bearer {refresh_token}"})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Invalid token type"


@pytest.mark.parametrize(
    "route",
    [route for route in app.routes if route.path.startswith("/api/")],
)
def test_missing_route_authentication(client, route):
    """
    This tests every registered API endpoint to ensure that it requires token authentication.
    """

    # There are some special endpoints that do not require authentication.
    if route.path in ["/api/ping", "/api/auth", "/api/auth/logout"]:
        return

    for method in route.methods:
        if method == "POST":
            client_method = client.post
        elif method == "GET":
            client_method = client.get
        elif method == "PATCH":
            client_method = client.patch
        elif method == "DELETE":
            client_method = client.delete
        else:
            raise ValueError(f"Test does not account for method: {method}")

        result = client_method(route.path)
        assert result.status_code == status.HTTP_401_UNAUTHORIZED, f"{method} on {route.path} does not require auth!"


#
# VALID TESTS
#


def test_auth_success(client: testclient.TestClient, db):
    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    access_token = auth.json()["access_token"]
    refresh_token = auth.json()["refresh_token"]
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["token_type"] == "bearer"
    assert access_token
    assert refresh_token
    assert auth.cookies.get("access_token")
    assert auth.cookies.get("refresh_token")

    # Attempt to use the token to access a protected API endpoint
    get = client.get("/api/user/", headers={"Authorization": f"Bearer {access_token}"})
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 1
