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
    refresh_token = auth.cookies.get("refresh_token")
    assert auth.status_code == status.HTTP_200_OK
    assert refresh_token

    # Wait for the token to expire
    time.sleep(expiration_seconds + 1)

    # Attempt to use the refresh token to obtain a new access token
    refresh = client.get("/api/auth/refresh", cookies={"refresh_token": refresh_token})
    assert refresh.status_code == status.HTTP_401_UNAUTHORIZED
    assert refresh.json()["detail"] == "Refresh token expired"


def test_invalid_token(client):
    refresh = client.get("/api/auth/refresh", cookies={"refresh_token": "Bearer asdf"})
    assert refresh.status_code == status.HTTP_401_UNAUTHORIZED
    assert refresh.json()["detail"] == "Invalid token"


def test_missing_token(client):
    refresh = client.get("/api/auth/refresh")
    assert refresh.status_code == status.HTTP_401_UNAUTHORIZED
    assert refresh.json()["detail"] == "Not authenticated"


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

    # Attempt to use the access token as a refresh token
    refresh = client.get("/api/auth/refresh", cookies={"refresh_token": access_token})
    assert refresh.status_code == status.HTTP_401_UNAUTHORIZED
    assert refresh.json()["detail"] == "Invalid token type"


#
# VALID TESTS
#


def test_auth_refresh_success(client, monkeypatch, requests_mock):
    # This is set to a fairly high number for the purposes of a unit test because PyJWT
    # and other JWT implementations usually allow for a small amount of leeway due to clock
    # drift when validating the tokens. Values less than 10 seconds here break the test.
    expiration_seconds = 10
    monkeypatch.setenv("JWT_ACCESS_EXPIRE_SECONDS", str(expiration_seconds))

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

    requests_mock.post(
        "http://db-api/api/user/validate_refresh_token",
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

    # Wait for the access token to expire
    time.sleep(expiration_seconds + 1)

    # Attempt to use the token to access a protected API endpoint now that the token is expired
    get = client.get("/api/user/", cookies={"access_token": access_token})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Access token expired"

    # Attempt to refresh the tokens
    refresh = client.get("/api/auth/refresh", cookies={"refresh_token": refresh_token})
    assert refresh.status_code == status.HTTP_200_OK
    new_access_token = refresh.cookies.get("access_token")
    new_refresh_token = refresh.cookies.get("refresh_token")
    assert new_access_token != access_token
    assert new_refresh_token != refresh_token

    # Attempt to use the new access token to access a protected API endpoint
    get = client.get("/api/user/", cookies={"access_token": new_access_token})
    assert get.status_code == status.HTTP_200_OK
