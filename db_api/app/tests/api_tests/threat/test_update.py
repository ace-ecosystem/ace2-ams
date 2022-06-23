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
        ("queues", None),
        ("queues", "test_queue"),
        ("queues", [123]),
        ("queues", [None]),
        ("queues", [""]),
        ("queues", ["abc", 123]),
        ("types", 123),
        ("types", None),
        ("types", "test_type"),
        ("types", [123]),
        ("types", [None]),
        ("types", [""]),
        ("types", ["abc", 123]),
        ("types", []),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/threat/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client):
    update = client.patch("/api/threat/1", json={"types": ["test_type"], "value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_update_duplicate_unique_fields(client, db, key):
    # Create some objects
    obj1 = factory.threat.create_or_read(value="test", types=["test_type"], db=db)
    obj2 = factory.threat.create_or_read(value="test2", types=["test_type"], db=db)

    # Ensure you cannot update a unique field to a value that already exists
    update = client.patch(f"/api/threat/{obj2.uuid}", json={key: getattr(obj1, key)})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/threat/{uuid.uuid4()}", json={"types": ["test_type"], "value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "values",
    [
        (["new_type"]),
        (["new_type1", "new_type2"]),
    ],
)
def test_update_valid_types(client, db, values):
    # Create the object
    initial_types = ["test_type1", "test_type2", "test_type3"]
    obj = factory.threat.create_or_read(value="test", types=initial_types, db=db)
    assert len(obj.types) == len(initial_types)

    # Create the new threat types
    for value in values:
        factory.threat_type.create_or_read(value=value, db=db)

    # Update it
    update = client.patch(f"/api/threat/{obj.uuid}", json={"types": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(obj.types) == len(values)


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", "test"),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client, db, key, initial_value, updated_value):
    # Create the object
    obj = factory.threat.create_or_read(value="test", types=["test_type"], db=db)

    # Set the initial value
    setattr(obj, key, initial_value)

    # Update it
    update = client.patch(f"/api/threat/{obj.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert getattr(obj, key) == updated_value


def test_update_queue(client, db):
    factory.queue.create_or_read(value="default", db=db)
    factory.queue.create_or_read(value="updated", db=db)

    # Create the object
    obj = factory.threat.create_or_read(value="test", queues=["default"], types=["test_type"], db=db)

    # Update it
    update = client.patch(f"/api/threat/{obj.uuid}", json={"queues": ["updated"]})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert obj.queues[0].value == "updated"
