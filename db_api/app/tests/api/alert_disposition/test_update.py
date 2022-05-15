import pytest
import uuid

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
        ("rank", 1.234),
        ("rank", "123"),
        ("rank", None),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/alert/disposition/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client):
    update = client.patch("/api/alert/disposition/1", json={"value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/alert/disposition/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", "test"),
        ("rank", 1, 2),
        ("rank", 1, 1),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client, db, key, initial_value, updated_value):
    # Create the object
    obj = factory.alert_disposition.create_or_read(value="test", rank=1, db=db)

    # Set the initial value
    setattr(obj, key, initial_value)

    # Update it
    update = client.patch(f"/api/alert/disposition/{obj.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert getattr(obj, key) == updated_value
