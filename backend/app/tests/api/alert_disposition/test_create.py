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
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {"rank": 1, "value": "test"}
    create_json[key] = value
    create = client_valid_access_token.post("/api/alert/disposition/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in create.text


@pytest.mark.parametrize(
    "key",
    [
        ("rank"),
        ("uuid"),
        ("value"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, key):
    # Create an object
    create1_json = {"rank": 1, "uuid": str(uuid.uuid4()), "value": "test"}
    client_valid_access_token.post("/api/alert/disposition/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"rank": 2, "value": "test2"}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/alert/disposition/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("rank"),
        ("value"),
    ],
)
def test_create_missing_required_fields(client_valid_access_token, key):
    create_json = {"rank": 1, "value": "test"}
    del create_json[key]
    create = client_valid_access_token.post("/api/alert/disposition/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in create.text


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("description", None), ("description", "test"), ("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client_valid_access_token, key, value):
    # Create the object
    create = client_valid_access_token.post("/api/alert/disposition/", json={key: value, "rank": 1, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client_valid_access_token):
    # Create the object
    create = client_valid_access_token.post("/api/alert/disposition/", json={"rank": 1, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["rank"] == 1
    assert get.json()["value"] == "test"
