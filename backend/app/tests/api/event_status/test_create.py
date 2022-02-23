import pytest
import uuid

from fastapi import status

from tests import helpers


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
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {"value": "test", "queues": ["default"]}
    create_json[key] = value
    create = client_valid_access_token.post("/api/event/status/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
        ("value"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, db, key):
    # Create an object
    helpers.create_queue(value="default", db=db)
    create1_json = {"uuid": str(uuid.uuid4()), "value": "test", "queues": ["default"]}
    client_valid_access_token.post("/api/event/status/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"value": "test2", "queues": ["default"]}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/event/status/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("queues"),
        ("value"),
    ],
)
def test_create_missing_required_fields(client_valid_access_token, db, key):
    helpers.create_queue(value="default", db=db)
    create_json = {"value": "test", "queues": ["default"]}
    del create_json[key]
    create = client_valid_access_token.post("/api/event/status/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("description", None), ("description", "test"), ("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client_valid_access_token, db, key, value):
    # Create the object
    helpers.create_queue(value="default", db=db)
    create = client_valid_access_token.post(
        "/api/event/status/", json={key: value, "value": "test", "queues": ["default"]}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client_valid_access_token, db):
    # Create the object
    helpers.create_queue(value="default", db=db)
    create = client_valid_access_token.post("/api/event/status/", json={"value": "test", "queues": ["default"]})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"
