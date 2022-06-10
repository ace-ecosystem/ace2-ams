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
        ("uuid", None),
        ("uuid", 1),
        ("uuid", "abc"),
        ("uuid", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client, db, key, value):
    factory.queue.create_or_read(value="default", db=db)
    create_json = {"value": "test", key: value}
    create = client.post("/api/node/threat_actor/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_create_missing_required_fields(client, key):
    create_json = {"value": "test"}
    del create_json[key]
    create = client.post("/api/node/threat_actor/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_queue(client):
    create = client.post("/api/node/threat_actor/", json={"value": "test", "queues": ["nonexistent_queue"]})
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("description", None), ("description", "test"), ("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client, db, key, value):
    # Create the object
    factory.queue.create_or_read(value="test_queue", db=db)
    create = client.post("/api/node/threat_actor/", json={key: value, "value": "test", "queues": ["test_queue"]})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client, db):
    # Create the object
    factory.queue.create_or_read(value="test_queue", db=db)
    create = client.post("/api/node/threat_actor/", json={"value": "test", "queues": ["test_queue"]})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"
