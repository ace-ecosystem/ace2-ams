import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/user/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/user/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client, db):
    # Create some users
    helpers.create_user(username="johndoe", email="johndoe@test.com", db=db)
    helpers.create_user(username="janedoe", email="janedoe@test.com", db=db)

    # Read them back
    get = client.get("/api/user/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 3  # There is by default an "analyst" user
