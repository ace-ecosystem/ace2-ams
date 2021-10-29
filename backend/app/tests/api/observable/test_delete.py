import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete("/api/observable/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete(f"/api/observable/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client_valid_access_token):
    # Create an observable type
    type_create = client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create the object
    create = client_valid_access_token.post("/api/observable/", json={"type": "test_type", "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client_valid_access_token.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the observable type is still there
    get = client_valid_access_token.get(type_create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_type"
