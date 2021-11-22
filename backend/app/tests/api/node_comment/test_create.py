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
        ("node_uuid", 123),
        ("node_uuid", None),
        ("node_uuid", ""),
        ("node_uuid", "abc"),
        ("user", 123),
        ("user", None),
        ("user", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client_valid_access_token, key, value):
    create = client_valid_access_token.post("/api/node/comment/", json={key: value})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_duplicate_node_uuid_value(client_valid_access_token, db):
    # Create a node
    node = helpers.create_alert(db=db)

    # Create a user
    helpers.create_user(username="johndoe", db=db)

    # Create a comment
    create_json = {
        "node_uuid": str(node.uuid),
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Make sure you cannot add the same comment value to a node
    create_json = {
        "node_uuid": str(node.uuid),
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, db, key):
    # Create a node
    node = helpers.create_alert(db=db)

    # Create a user
    helpers.create_user(username="johndoe", db=db)

    # Create a comment
    create1_json = {
        "node_uuid": str(node.uuid),
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    client_valid_access_token.post("/api/node/comment/", json=create1_json)

    # Ensure you cannot create another comment with the same unique field value
    create2_json = {
        "node_uuid": str(node.uuid),
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test2",
    }
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/node/comment/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_node_uuid(client_valid_access_token, db):
    # Create a user
    helpers.create_user(username="johndoe", db=db)

    # Create a comment
    create_json = {
        "node_uuid": str(uuid.uuid4()),
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_nonexistent_user(client_valid_access_token, db):
    # Create a node
    node = helpers.create_alert(db=db)

    # Create a comment
    create_json = {
        "node_uuid": str(node.uuid),
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_create_valid_required_fields(client_valid_access_token, db):
    # Create a node
    node = helpers.create_alert(db=db)
    initial_node_version = node.version

    # Create a user
    helpers.create_user(username="johndoe", db=db)

    # Create a comment
    create_json = {
        "node_uuid": str(node.uuid),
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED
    assert len(node.comments) == 1
    assert node.comments[0].value == "test"
    assert node.version != initial_node_version
