import pytest
import uuid

from fastapi import status


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


def test_create_duplicate_node_uuid_value(client_valid_access_token):
    # Create a node
    node_uuid = str(uuid.uuid4())
    node_create = client_valid_access_token.post("/api/analysis/", json={"uuid": node_uuid})

    # Read the node back
    get_node = client_valid_access_token.get(node_create.headers["Content-Location"])
    assert get_node.json()["comments"] == []

    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create a user
    create_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    client_valid_access_token.post("/api/user/", json=create_json)

    # Create a comment
    create_json = {
        "node_uuid": node_uuid,
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Make sure you cannot add the same comment value to a node
    create_json = {
        "node_uuid": node_uuid,
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
def test_create_duplicate_unique_fields(client_valid_access_token, key):
    # Create a node
    node_uuid = str(uuid.uuid4())
    client_valid_access_token.post("/api/analysis/", json={"uuid": node_uuid})

    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create a user
    create_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    client_valid_access_token.post("/api/user/", json=create_json)

    # Create a comment
    create1_json = {
        "node_uuid": node_uuid,
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    client_valid_access_token.post("/api/node/comment/", json=create1_json)

    # Ensure you cannot create another comment with the same unique field value
    create2_json = {
        "node_uuid": node_uuid,
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test2",
    }
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/node/comment/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_node_uuid(client_valid_access_token):
    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create a user
    create_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    client_valid_access_token.post("/api/user/", json=create_json)

    # Create a comment
    create_json = {
        "node_uuid": str(uuid.uuid4()),
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_nonexistent_user(client_valid_access_token):
    # Create a node
    node_uuid = str(uuid.uuid4())
    client_valid_access_token.post("/api/analysis/", json={"uuid": node_uuid})

    # Create a comment
    create_json = {
        "node_uuid": node_uuid,
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_create_valid_required_fields(client_valid_access_token):
    # Create a node
    node_uuid = str(uuid.uuid4())
    node_create = client_valid_access_token.post("/api/analysis/", json={"uuid": node_uuid})

    # Read the node back
    get_node = client_valid_access_token.get(node_create.headers["Content-Location"])
    initial_node_version = get_node.json()["version"]
    assert get_node.json()["comments"] == []

    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create a user
    create_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    client_valid_access_token.post("/api/user/", json=create_json)

    # Create a comment
    create_json = {
        "node_uuid": node_uuid,
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read the node back
    get_node = client_valid_access_token.get(node_create.headers["Content-Location"])
    assert get_node.json()["version"] != initial_node_version
    assert get_node.json()["comments"][0]["value"] == "test"
