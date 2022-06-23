import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/observable/relationship/type/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/observable/relationship/type/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


def test_delete_used(client, db):
    # Create an object
    obj = factory.observable_relationship_type.create_or_read(value="test", db=db)

    # Assign it to another object
    alert = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert.root_analysis, db=db)
    obs2 = factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert.root_analysis, db=db)

    factory.observable_relationship.create_or_read(observable=obs1, related_observable=obs2, type="test", db=db)

    # Ensure you cannot delete it now that it is in use
    delete = client.delete(f"/api/observable/relationship/type/{obj.uuid}")
    assert delete.status_code == status.HTTP_400_BAD_REQUEST


#
# VALID TESTS
#


def test_delete(client, db):
    # Create the object
    obj = factory.observable_relationship_type.create_or_read(value="test", db=db)

    # Delete it
    delete = client.delete(f"/api/observable/relationship/type/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
