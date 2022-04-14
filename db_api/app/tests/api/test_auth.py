import pytest

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "username,password",
    [
        ("analyst", "wrongpassword"),
        ("wronguser", "asdfasdf"),
    ],
)
def test_auth_invalid(client, username, password):
    auth = client.post("/api/auth", json={"username": username, "password": password, "new_refresh_token": "asdf"})
    assert auth.status_code == status.HTTP_401_UNAUTHORIZED
    assert auth.json()["detail"] == "Invalid username or password"


def test_disabled_user(client, db):
    user = helpers.create_user(username="johndoe", password="abcd1234", db=db)

    # Attempt to authenticate
    auth = client.post("/api/auth", json={"username": "johndoe", "password": "abcd1234", "new_refresh_token": "asdf"})
    assert auth.status_code == status.HTTP_200_OK

    # Disable the user
    user.enabled = False

    # However, they will not be able to authenticate again to receive a new token.
    auth = client.post("/api/auth", json={"username": "johndoe", "password": "abcd1234", "new_refresh_token": "asdf"})
    assert auth.status_code == status.HTTP_401_UNAUTHORIZED
    assert auth.json()["detail"] == "Invalid username or password"


@pytest.mark.parametrize(
    "key",
    [
        ("username"),
        ("password"),
        ("new_refresh_token"),
    ],
)
def test_missing_required_fields(client, key):
    create_json = {"username": "johndoe", "password": "abcd1234", "new_refresh_token": "asdf"}
    del create_json[key]
    create = client.post("/api/auth", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# VALID TESTS
#


def test_auth_success(client):
    auth = client.post("/api/auth", json={"username": "analyst", "password": "asdfasdf", "new_refresh_token": "asdf"})
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["username"] == "analyst"
