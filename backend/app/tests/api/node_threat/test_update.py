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
def test_update_duplicate_unique_fields(client_valid_access_token, db, key):
    # Create a node threat type
    obj1 = helpers.create_node_threat(value="test", types=["test_type"], db=db)
    obj2 = helpers.create_node_threat(value="test2", types=["test_type"], db=db)

    # Ensure you cannot update a unique field to a value that already exists
    update = client_valid_access_token.patch(f"/api/node/threat/{obj2.uuid}", json={key: getattr(obj1, key)})
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
    "values",
    [
        (["new_type"]),
        (["new_type1", "new_type2"]),
    ],
)
def test_update_valid_types(client_valid_access_token, db, values):
    # Create the object
    initial_types = ["test_type1", "test_type2", "test_type3"]
    obj = helpers.create_node_threat(value="test", types=initial_types, db=db)
    assert len(obj.types) == len(initial_types)

    # Create the new node threat types
    for value in values:
        helpers.create_node_threat_type(value=value, db=db)

    # Update it
    update = client_valid_access_token.patch(f"/api/node/threat/{obj.uuid}", json={"types": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(obj.types) == len(values)


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", "test"),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client_valid_access_token, db, key, initial_value, updated_value):
    # Create the object
    obj = helpers.create_node_threat(value="test", types=["test_type"], db=db)

    # Set the initial value
    setattr(obj, key, initial_value)

    # Update it
    update = client_valid_access_token.patch(f"/api/node/threat/{obj.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert getattr(obj, key) == updated_value
