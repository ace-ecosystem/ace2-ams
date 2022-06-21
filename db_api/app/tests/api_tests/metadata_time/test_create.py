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
        ("value", None),
        ("value", ""),
        ("value", "Monday"),
        ("value", "2022-01-01"),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {"value": "2022-01-01T00:00:00Z", key: value}
    create = client.post("/api/metadata/time/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_create_missing_required_fields(client, key):
    create_json = {"value": "2022-01-01T00:00:00Z"}
    del create_json[key]
    create = client.post("/api/metadata/time/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("description", None), ("description", "test"), ("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client, key, value):
    # Create the object
    create = client.post("/api/metadata/time/", json={key: value, "value": "2022-01-01T00:00:00Z"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client):
    # Create the object
    create = client.post("/api/metadata/time/", json={"value": "2022-01-01T00:00:00Z"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == "2022-01-01T00:00:00+00:00"
