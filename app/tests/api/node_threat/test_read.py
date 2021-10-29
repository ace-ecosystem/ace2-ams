import uuid

from fastapi import status


#
# INVALID TESTS
#


def test_get_invalid_uuid(client_valid_access_token):
    get = client_valid_access_token.get("/api/node/threat/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client_valid_access_token):
    get = client_valid_access_token.get(f"/api/node/threat/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client_valid_access_token):
    # Create a node threat type
    client_valid_access_token.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create some objects
    client_valid_access_token.post("/api/node/threat/", json={"types": ["test_type"], "value": "test"})
    client_valid_access_token.post("/api/node/threat/", json={"types": ["test_type"], "value": "test2"})

    # Read them back
    get = client_valid_access_token.get("/api/node/threat/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_empty(client_valid_access_token):
    get = client_valid_access_token.get("/api/node/threat/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []
