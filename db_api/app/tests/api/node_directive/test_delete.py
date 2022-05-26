import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/node/directive/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/node/directive/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


def test_delete_used(client, db):
    # Create an object
    obj = factory.node_directive.create_or_read(value="test", db=db)

    # Assign it to another object
    alert = factory.alert.create(db=db)
    factory.observable.create_or_read(
        type="test", value="test", parent_analysis=alert.root_analysis, directives=["test"], db=db
    )

    # Ensure you cannot delete it now that it is in use
    delete = client.delete(f"/api/node/directive/{obj.uuid}")
    assert delete.status_code == status.HTTP_400_BAD_REQUEST


#
# VALID TESTS
#


def test_delete(client, db):
    # Create the object
    obj = factory.node_directive.create_or_read(value="test", db=db)

    # Delete it
    delete = client.delete(f"/api/node/directive/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
