import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/user/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/user/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_validate_refresh_token_disabled_user(client, db):
    factory.user.create_or_read(username="johndoe", email="johndoe@test.com", enabled=False, db=db)

    # Try to validate the refresh token
    auth = client.post(
        "/api/user/validate_refresh_token",
        json={"username": "johndoe", "refresh_token": "asdf", "new_refresh_token": "1234"},
    )
    assert auth.status_code == status.HTTP_401_UNAUTHORIZED


def test_validate_refresh_token_invalid_token(client, db):
    factory.user.create_or_read(username="johndoe", email="johndoe@test.com", refresh_token="asdf", db=db)

    # Try to validate the refresh token
    auth = client.post(
        "/api/user/validate_refresh_token",
        json={"username": "johndoe", "refresh_token": "wxyz", "new_refresh_token": "1234"},
    )
    assert auth.status_code == status.HTTP_401_UNAUTHORIZED


def test_validate_refresh_token_nonexistent_user(client, db):
    # Try to validate the refresh token
    auth = client.post(
        "/api/user/validate_refresh_token",
        json={"username": "johndoe", "refresh_token": "asdf", "new_refresh_token": "1234"},
    )
    assert auth.status_code == status.HTTP_401_UNAUTHORIZED


#
# VALID TESTS
#


def test_get_all(client, db):
    # Create some users
    factory.user.create_or_read(username="johndoe", email="johndoe@test.com", enabled=False, db=db)
    factory.user.create_or_read(username="janedoe", email="janedoe@test.com", db=db)

    # Read them back
    get = client.get("/api/user/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 3  # There is by default an "analyst" user

    # Filter by enabled
    get = client.get("/api/user/?enabled=True")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 2  # There is by default an "analyst" user

    # Filter by username
    get = client.get("/api/user/?username=janedoe")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 1


def test_validate_refresh_token(client, db):
    factory.user.create_or_read(username="johndoe", email="johndoe@test.com", refresh_token="asdf", db=db)

    # Try to validate the refresh token
    auth = client.post(
        "/api/user/validate_refresh_token",
        json={"username": "johndoe", "refresh_token": "asdf", "new_refresh_token": "1234"},
    )
    assert auth.status_code == status.HTTP_200_OK

    # Make sure that the new_refresh_token is the one that works now
    auth = client.post(
        "/api/user/validate_refresh_token",
        json={"username": "johndoe", "refresh_token": "1234", "new_refresh_token": "wxyz"},
    )
    assert auth.status_code == status.HTTP_200_OK
