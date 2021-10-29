import pytest
import uuid

from fastapi import status


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", 123),
        ("description", ""),
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
    create_json = {"value": "test"}
    create_json[key] = value
    create = client_valid_access_token.post("/api/alert/queue/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
        ("value"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, key):
    # Create an object
    create1_json = {"uuid": str(uuid.uuid4()), "value": "test"}
    client_valid_access_token.post("/api/alert/queue/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"value": "test2"}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/alert/queue/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_create_missing_required_fields(client_valid_access_token, key):
    create_json = {"value": "test"}
    del create_json[key]
    create = client_valid_access_token.post("/api/alert/queue/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("description", None), ("description", "test"), ("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client_valid_access_token, key, value):
    # Create the object
    create = client_valid_access_token.post("/api/alert/queue/", json={key: value, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client_valid_access_token):
    # Create the object
    create = client_valid_access_token.post("/api/alert/queue/", json={"value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"
