import pytest
import uuid

from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from fastapi import status

from tests import factory


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", 123),
        ("description", ""),
        ("value", None),
        ("value", ""),
        ("value", "Monday"),
        ("value", "2022-01-01"),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/metadata/time/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client):
    update = client.patch("/api/metadata/time/1", json={"value": "2022-01-01T00:00:00Z"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_unique_fields(client, db):
    # Create some objects
    now = "2021-01-01T00:00:00+00:00"
    later = "2022-01-01T00:00:00+00:00"

    obj1 = factory.metadata_time.create_or_read(value=parse(now), db=db)
    obj2 = factory.metadata_time.create_or_read(value=parse(later), db=db)

    # Ensure you cannot update a unique field to a value that already exists
    update = client.patch(f"/api/metadata/time/{obj2.uuid}", json={"value": now})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/metadata/time/{uuid.uuid4()}", json={"value": "2022-01-01T00:00:00Z"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", "test"),
        ("value", "2021-01-01T00:00:00+00:00", 1640995200),
        ("value", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("value", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00+00:00"),
        ("value", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000+00:00"),
        ("value", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
    ],
)
def test_update(client, db, key, initial_value, updated_value):
    # Create the object
    obj = factory.metadata_time.create_or_read(value=datetime.now(timezone.utc), db=db)

    # Set the initial value
    setattr(obj, key, initial_value)

    # Update it
    update = client.patch(f"/api/metadata/time/{obj.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if key == "value":
        assert obj.value == parse("2022-01-01T00:00:00+00:00")
    else:
        assert getattr(obj, key) == updated_value
