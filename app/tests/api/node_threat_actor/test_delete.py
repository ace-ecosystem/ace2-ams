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
    delete = client_valid_access_token.delete("/api/node/threat_actor/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete(f"/api/node/threat_actor/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client_valid_access_token):
    # Create the object
    create = client_valid_access_token.post("/api/node/threat_actor/", json={"value": "test"})
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
