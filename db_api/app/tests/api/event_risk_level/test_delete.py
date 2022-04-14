import uuid

from fastapi import status

from tests import helpers


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/event/risk_level/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/event/risk_level/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client, db):
    # Create the object
    obj = helpers.create_event_risk_level(value="test", db=db)

    # Read it back
    get = client.get(f"/api/event/risk_level/{obj.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client.delete(f"/api/event/risk_level/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/event/risk_level/{obj.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND
