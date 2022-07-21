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
        ("rank", 1.234),
        ("rank", "123"),
        ("rank", None),
        ("uuid", None),
        ("uuid", 1),
        ("uuid", "abc"),
        ("uuid", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {"rank": 1, "value": "test", key: value}
    create = client.post("/api/alert/disposition/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in create.text


@pytest.mark.parametrize(
    "key",
    [
        ("rank"),
        ("value"),
    ],
)
def test_create_missing_required_fields(client, key):
    create_json = {"rank": 1, "value": "test"}
    del create_json[key]
    create = client.post("/api/alert/disposition/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in create.text


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("description", None), ("description", "test"), ("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client, key, value):
    # Create the object
    create = client.post("/api/alert/disposition/", json={key: value, "rank": 1, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client):
    # Create the object
    create = client.post("/api/alert/disposition/", json={"rank": 1, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["rank"] == 1
    assert get.json()["value"] == "test"
