import uuid

from fastapi import status

from tests import factory


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/node/directive/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/node/directive/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client, db):
    # Create the object
    obj = factory.node_directive.create_or_read(value="test", db=db)

    # Read it back
    get = client.get(f"/api/node/directive/{obj.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client.delete(f"/api/node/directive/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/node/directive/{obj.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND
