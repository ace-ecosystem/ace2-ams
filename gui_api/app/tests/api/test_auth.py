import pytest
import time

from fastapi import status
from uuid import uuid4

from main import app


#
# INVALID TESTS
#


def test_expired_token(client, monkeypatch, requests_mock):
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

    requests_mock.get(f"http://db-api/api/user/", json={"items": [], "total": 0, "limit": 50, "offset": 0})

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "analyst", "password": "asdfasdf"})
    access_token = auth.cookies.get("access_token")
    assert auth.status_code == status.HTTP_200_OK
    assert access_token

    # Attempt to use the token to access a protected API endpoint
    get = client.get("/api/user/", cookies={"access_token": access_token})
    assert get.status_code == status.HTTP_200_OK

    # Wait for the token to expire
    time.sleep(expiration_seconds + 1)

    # Attempt to use the token to access a protected API endpoint now that the token is expired
    get = client.get("/api/user/", cookies={"access_token": access_token})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Access token expired"


def test_invalid_token(client):
    get = client.get("/api/user/", cookies={"access_token": "Bearer asdf"})
    assert get.status_code == status.HTTP_401_UNAUTHORIZED
    assert get.json()["detail"] == "Invalid token"


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
    refresh_token = auth.cookies.get("refresh_token")
    assert auth.status_code == status.HTTP_200_OK
    assert refresh_token

    # Attempt to use the refresh token to access a protected API endpoint
    get = client.get("/api/user/", cookies={"access_token": refresh_token})
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
    if route.path in [
        "/api/ping",
        "/api/auth",
        "/api/auth/logout",
        "/api/test/add_alerts",
        "/api/test/add_event",
        "/api/test/reset_database",
    ]:
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


def test_auth_success(client, requests_mock):
    # Attempt to access a protected API endpoint
    get = client.get("/api/user/")
    assert get.status_code == status.HTTP_401_UNAUTHORIZED

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
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["username"] == "analyst"
    assert auth.cookies.get("access_token")
    assert auth.cookies.get("refresh_token")

    # Attempt to use the token to access a protected API endpoint
    get = client.get("/api/user/", cookies=auth.cookies)
    assert get.status_code == status.HTTP_200_OK
