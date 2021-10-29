import time

from fastapi import status

from core.config import Settings
from tests.helpers import create_test_user


#
# INVALID TESTS


def test_auth_validate_invalid_token(client):
    get = client.get("/api/auth/validate", headers={"Authorization": "Bearer asdf"})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Invalid token"


def test_expired_token(client, db, monkeypatch):
    def mock_get_settings():
        settings = Settings()
        settings.jwt_refresh_expire_seconds = 1
        return settings

    # Patching __code__ works no matter how the function is imported
    monkeypatch.setattr("core.config.get_settings.__code__", mock_get_settings.__code__)

    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    access_token = auth.json()["access_token"]
    refresh_token = auth.json()["refresh_token"]
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["token_type"] == "bearer"
    assert access_token

    # Attempt to use the token to access a protected API endpoint
    get = client.get("/api/user/", headers={"Authorization": f"Bearer {access_token}"})
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 1

    # Wait for the token to expire
    time.sleep(2)

    # Attempt to use the token to validate now that the token is expired
    get = client.get("/api/auth/validate", headers={"Authorization": f"Bearer {refresh_token}"})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Refresh token expired"


def test_missing_token(client):
    # Attempt to validate without supplying a refresh token
    get = client.get("/api/auth/validate")
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Not authenticated"


def test_wrong_token_type(client, db):
    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    access_token = auth.json()["access_token"]
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["token_type"] == "bearer"
    assert access_token

    # Attempt to use the access token to validate
    get = client.get("/api/auth/validate", headers={"Authorization": f"Bearer {access_token}"})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Invalid token type"


#
# VALID TESTS
#


def test_auth_validate_success(client, db):
    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    access_token = auth.json()["access_token"]
    refresh_token = auth.json()["refresh_token"]
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["token_type"] == "bearer"
    assert access_token
    assert refresh_token
    # Because the cookie values have a space in them, the entire string is quoted.
    assert auth.cookies["access_token"] == f'"Bearer {access_token}"'
    assert auth.cookies["refresh_token"] == f'"Bearer {refresh_token}"'

    # Attempt to use the refresh token to validate
    validate = client.get("/api/auth/validate", headers={"Authorization": f"Bearer {refresh_token}"})
    assert validate.status_code == status.HTTP_200_OK
    assert validate.json() is None
