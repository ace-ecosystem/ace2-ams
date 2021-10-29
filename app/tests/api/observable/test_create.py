import pytest
import uuid

from fastapi import status


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("expires_on", ""),
        ("expires_on", "Monday"),
        ("expires_on", "2022-01-01"),
        ("for_detection", 123),
        ("for_detection", None),
        ("for_detection", "True"),
        ("type", 123),
        ("type", None),
        ("type", ""),
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
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {"type": "test_type", "value": "test"}
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, key):
    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an object
    create1_json = {"type": "test_type", "uuid": str(uuid.uuid4()), "value": "test"}
    client_valid_access_token.post("/api/observable/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"type": "test_type", "value": "test2"}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/observable/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_duplicate_type_value(client_valid_access_token):
    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an object
    client_valid_access_token.post("/api/observable/", json={"type": "test_type", "value": "test"})

    # Ensure you cannot create another observable with the same unique type+value combination
    create = client_valid_access_token.post("/api/observable/", json={"type": "test_type", "value": "test"})
    assert create.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("type"),
        ("value"),
    ],
)
def test_create_missing_required_fields(client_valid_access_token, key):
    create_json = {"type": "test_type", "value": "test"}
    del create_json[key]
    create = client_valid_access_token.post("/api/observable/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_type(client_valid_access_token):
    create = client_valid_access_token.post("/api/observable/", json={"type": "test_type", "value": "test"})
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("expires_on", None),
        ("expires_on", 1640995200),
        ("expires_on", "2022-01-01T00:00:00Z"),
        ("expires_on", "2022-01-01 00:00:00"),
        ("expires_on", "2022-01-01 00:00:00.000000"),
        ("expires_on", "2021-12-31 19:00:00-05:00"),
        ("for_detection", False),
        ("for_detection", True),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client_valid_access_token, key, value):
    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create the object
    create = client_valid_access_token.post("/api/observable/", json={key: value, "type": "test_type", "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if key == "expires_on" and value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == value


def test_create_valid_required_fields(client_valid_access_token):
    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create the object
    create = client_valid_access_token.post("/api/observable/", json={"type": "test_type", "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"
