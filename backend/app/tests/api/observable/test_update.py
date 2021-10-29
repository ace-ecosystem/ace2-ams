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
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/observable/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/observable/1", json={"types": ["test_type"], "value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_type_value(client_valid_access_token):
    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create some observables
    client_valid_access_token.post("/api/observable/", json={"type": "test_type", "value": "test"})
    create = client_valid_access_token.post("/api/observable/", json={"type": "test_type", "value": "test2"})

    # Ensure you cannot update an observable to have a duplicate type+value combination
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(
        f"/api/observable/{uuid.uuid4()}", json={"type": "test_type", "value": "test"}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_valid_type(client_valid_access_token):
    # Create some observable types
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type2"})

    # Create the object
    create = client_valid_access_token.post("/api/observable/", json={"type": "test_type", "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["type"]["value"] == "test_type"

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"type": "test_type2"})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["type"]["value"] == "test_type2"


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("expires_on", 1640995200, 1640995200),
        ("expires_on", None, 1640995200),
        ("expires_on", None, "2022-01-01T00:00:00Z"),
        ("expires_on", None, "2022-01-01 00:00:00"),
        ("expires_on", None, "2022-01-01 00:00:00.000000"),
        ("expires_on", None, "2021-12-31 19:00:00-05:00"),
        ("expires_on", 1640995200, None),
        ("for_detection", True, False),
        ("for_detection", True, True),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client_valid_access_token, key, initial_value, updated_value):
    # Create some observable types
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type2"})

    # Create the object
    create_json = {"type": "test_type", "value": "test"}
    create_json[key] = initial_value
    create = client_valid_access_token.post("/api/observable/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if key == "expires_on" and initial_value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == initial_value

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if key == "expires_on" and updated_value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == updated_value
