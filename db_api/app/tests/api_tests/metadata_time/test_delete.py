import uuid

from datetime import datetime, timezone
from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/metadata/time/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/metadata/time/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


def test_delete_used(client, db):
    # Create an object
    now = datetime.now(timezone.utc)
    obj = factory.metadata_time.create_or_read(value=now, db=db)

    # Assign it to another object
    submission = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="test", value="test", parent_analysis=submission.root_analysis, time=now, db=db
    )

    # Ensure you cannot delete it now that it is in use
    delete = client.delete(f"/api/metadata/time/{obj.uuid}")
    assert delete.status_code == status.HTTP_400_BAD_REQUEST


#
# VALID TESTS
#


def test_delete(client, db):
    # Create the object
    obj = factory.metadata_time.create_or_read(value=datetime.now(timezone.utc), db=db)

    # Delete it
    delete = client.delete(f"/api/metadata/time/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
