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
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/node/threat/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/node/threat/1", json={"types": ["test_type"], "value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_update_duplicate_unique_fields(client_valid_access_token, key):
    # Create a node threat type
    client_valid_access_token.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create some objects
    create1_json = {"types": ["test_type"], "value": "test"}
    client_valid_access_token.post("/api/node/threat/", json=create1_json)

    create2_json = {"types": ["test_type"], "value": "test2"}
    create2 = client_valid_access_token.post("/api/node/threat/", json=create2_json)

    # Ensure you cannot update a unique field to a value that already exists
    update = client_valid_access_token.patch(create2.headers["Content-Location"], json={key: create1_json[key]})
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(
        f"/api/node/threat/{uuid.uuid4()}", json={"types": ["test_type"], "value": "test"}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "value",
    [
        (["new_type"]),
        (["new_type1", "new_type2"]),
    ],
)
def test_update_valid_types(client_valid_access_token, value):
    # Create some node threat types
    initial_types = ["test_type1", "test_type2", "test_type3"]
    for threat_type in initial_types:
        client_valid_access_token.post("/api/node/threat/type/", json={"value": threat_type})

    # Create the object
    create = client_valid_access_token.post("/api/node/threat/", json={"types": initial_types, "value": "test"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["types"]) == len(initial_types)

    # Create the new node threat types
    for threat_type in value:
        client_valid_access_token.post("/api/node/threat/type/", json={"value": threat_type})

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"types": value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["types"]) == len(value)


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", "test"),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client_valid_access_token, key, initial_value, updated_value):
    # Create a node threat type
    client_valid_access_token.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create the object
    create_json = {"types": ["test_type"], "value": "test"}
    create_json[key] = initial_value
    create = client_valid_access_token.post("/api/node/threat/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == initial_value

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == updated_value
