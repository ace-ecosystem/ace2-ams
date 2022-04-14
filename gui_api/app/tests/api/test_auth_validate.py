import time

from fastapi import status
from uuid import uuid4


#
# INVALID TESTS


def test_expired_token(client, monkeypatch, requests_mock):
    # This is set to a fairly high number for the purposes of a unit test because PyJWT
    # and other JWT implementations usually allow for a small amount of leeway due to clock
    # drift when validating the tokens. Values less than 10 seconds here break the test.
    expiration_seconds = 10
    monkeypatch.setenv("JWT_REFRESH_EXPIRE_SECONDS", str(expiration_seconds))

    requests_mock.post(
        "http://db-api/api/auth",
        json={
            "default_alert_queue": {"value": "queue1", "uuid": str(uuid4())},
            "default_event_queue": {"value": "queue1", "uuid": str(uuid4())},
            "display_name": "Analyst",
            "email": "analyst@test.com",
            "roles": [],
            "username": "analyst",
            "uuid": str(uuid4()),
        },
    )

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "analyst", "password": "asdfasdf"})
    access_token = auth.cookies.get("access_token")
    refresh_token = auth.cookies.get("refresh_token")
    assert auth.status_code == status.HTTP_200_OK
    assert access_token
    assert refresh_token

    # Attempt to validate the token
    get = client.get("/api/auth/validate", cookies={"refresh_token": refresh_token})
    assert get.status_code == status.HTTP_200_OK

    # Wait for the token to expire
    time.sleep(expiration_seconds + 1)

    # Attempt to validate the token now that it is expired
    get = client.get("/api/auth/validate", cookies={"refresh_token": refresh_token})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Refresh token expired"


def test_invalid_token(client):
    get = client.get("/api/auth/validate", cookies={"refresh_token": "Bearer asdf"})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Invalid token"


def test_missing_token(client):
    get = client.get("/api/auth/validate")
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Not authenticated"


def test_wrong_token_type(client, requests_mock):
    requests_mock.post(
        "http://db-api/api/auth",
        json={
            "default_alert_queue": {"value": "queue1", "uuid": str(uuid4())},
            "default_event_queue": {"value": "queue1", "uuid": str(uuid4())},
            "display_name": "Analyst",
            "email": "analyst@test.com",
            "roles": [],
            "username": "analyst",
            "uuid": str(uuid4()),
        },
    )

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "analyst", "password": "asdfasdf"})
    access_token = auth.cookies.get("access_token")
    assert auth.status_code == status.HTTP_200_OK
    assert access_token

    # Attempt to use the access token to validate
    get = client.get("/api/auth/validate", cookies={"refresh_token": access_token})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Invalid token type"


#
# VALID TESTS
#


def test_auth_validate_success(client, requests_mock):
    requests_mock.post(
        "http://db-api/api/auth",
        json={
            "default_alert_queue": {"value": "queue1", "uuid": str(uuid4())},
            "default_event_queue": {"value": "queue1", "uuid": str(uuid4())},
            "display_name": "Analyst",
            "email": "analyst@test.com",
            "roles": [],
            "username": "analyst",
            "uuid": str(uuid4()),
        },
    )

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "analyst", "password": "asdfasdf"})
    refresh_token = auth.cookies.get("refresh_token")
    assert auth.status_code == status.HTTP_200_OK
    assert refresh_token

    # Attempt to use the access token to validate
    get = client.get("/api/auth/validate", cookies={"refresh_token": refresh_token})
    assert get.status_code == status.HTTP_200_OK
