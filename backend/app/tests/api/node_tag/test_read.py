import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client_valid_access_token):
    get = client_valid_access_token.get("/api/node/tag/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client_valid_access_token):
    get = client_valid_access_token.get(f"/api/node/tag/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client_valid_access_token, db):
    # Create some objects
    helpers.create_node_tag(value="test", db=db)
    helpers.create_node_tag(value="test2", db=db)

    # Read them back
    get = client_valid_access_token.get("/api/node/tag/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_empty(client_valid_access_token):
    get = client_valid_access_token.get("/api/node/tag/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []
