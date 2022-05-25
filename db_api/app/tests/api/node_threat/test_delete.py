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
    delete = client.delete("/api/node/threat/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/node/threat/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client, db):
    # Create a node threat type
    threat_type = factory.node_threat_type.create_or_read(value="test_type", db=db)

    # Create a node threat
    threat = factory.node_threat.create_or_read(value="test", types=["test_type"], db=db)

    # Delete it
    delete = client.delete(f"/api/node/threat/{threat.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/node/threat/{threat.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the node threat type is still there
    get = client.get(f"/api/node/threat/type/{threat_type.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_type"
