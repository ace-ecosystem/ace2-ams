import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/analysis/module_type/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/analysis/module_type/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


def test_delete_used(client, db):
    # Create an object
    obj = factory.analysis_module_type.create_or_read(value="test", db=db)

    # Assign it to another object
    alert = factory.alert.create(db=db)
    observable = factory.observable.create_or_read(
        type="test", value="test", parent_analysis=alert.root_analysis, db=db
    )
    factory.analysis.create_or_read(analysis_module_type=obj, submission=alert, target=observable, db=db)

    # Ensure you cannot delete it now that it is in use
    delete = client.delete(f"/api/analysis/module_type/{obj.uuid}")
    assert delete.status_code == status.HTTP_400_BAD_REQUEST


#
# VALID TESTS
#


def test_delete(client, db):
    # Create an object
    obj = factory.analysis_module_type.create_or_read(value="test", db=db)

    # Delete it
    delete = client.delete(f"/api/analysis/module_type/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
