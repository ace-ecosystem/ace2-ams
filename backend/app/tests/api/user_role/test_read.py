import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client_valid_access_token):
    get = client_valid_access_token.get("/api/user/role/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client_valid_access_token):
    get = client_valid_access_token.get(f"/api/user/role/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client_valid_access_token, db):
    # Create some objects
    helpers.create_user_role(value="test_role", db=db)
    helpers.create_user_role(value="test_role2", db=db)

    # Read them back
    get = client_valid_access_token.get("/api/user/role/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 2


def test_get_all_empty(client_valid_access_token):
    get = client_valid_access_token.get("/api/user/role/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 0
