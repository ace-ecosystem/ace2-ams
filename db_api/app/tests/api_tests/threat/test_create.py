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
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("uuid", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client, db, key, value):
    create_json = {"types": ["test_type"], "value": "test", "queues": ["external"], key: value}

    create = client.post("/api/threat/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("queues"),
        ("types"),
        ("value"),
    ],
)
def test_create_missing_required_fields(client, db, key):
    create_json = {"types": ["test_type"], "value": "test", "queues": ["external"]}
    del create_json[key]
    create = client.post("/api/threat/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_queue(client, db):
    factory.threat_type.create_or_read(value="test_type", db=db)
    create = client.post(
        "/api/threat/", json={"types": ["test_type"], "value": "test", "queues": ["nonexistent_queue"]}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_nonexistent_type(client, db):
    create = client.post("/api/threat/", json={"types": ["test_type"], "value": "test", "queues": ["external"]})
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", None),
        ("description", "test"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client, db, key, value):
    factory.threat_type.create_or_read(value="test_type", db=db)

    # Create the object
    create = client.post(
        "/api/threat/", json={key: value, "types": ["test_type"], "value": "test", "queues": ["external"]}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


@pytest.mark.parametrize(
    "values,list_length",
    [
        (["test_type"], 1),
        (["test_type1", "test_type2"], 2),
        (["test_type", "test_type"], 1),
    ],
)
def test_create_valid_types(client, db, values, list_length):
    for value in values:
        factory.threat_type.create_or_read(value=value, db=db)

    # Create the object
    create = client.post("/api/threat/", json={"types": values, "value": "test", "queues": ["external"]})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()["types"]) == list_length


def test_create_valid_required_fields(client, db):
    factory.threat_type.create_or_read(value="test_type", db=db)

    # Create the object
    create = client.post("/api/threat/", json={"types": ["test_type"], "value": "test", "queues": ["external"]})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"
