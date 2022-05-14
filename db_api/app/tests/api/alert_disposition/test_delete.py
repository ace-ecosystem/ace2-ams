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
    delete = client.delete("/api/alert/disposition/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/alert/disposition/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_400_BAD_REQUEST


#
# VALID TESTS
#


def test_delete(client, db):
    # Create the object
    obj = factory.alert_disposition.create(value="test", rank=1, db=db)

    # Delete it
    delete = client.delete(f"/api/alert/disposition/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
