import pytest
import uuid

from fastapi import status


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("value", None),
        ("value", 123),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/node/comment/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/node/comment/1", json={"value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/node/comment/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_duplicate_node_uuid_value(client_valid_access_token):
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

    # Create some comments
    create_json = {
        "node_uuid": node_uuid,
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client_valid_access_token.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    create2_json = {
        "node_uuid": node_uuid,
        "user": "johndoe",
        "uuid": str(uuid.uuid4()),
        "value": "test2",
    }
    create2 = client_valid_access_token.post("/api/node/comment/", json=create2_json)
    assert create2.status_code == status.HTTP_201_CREATED

    # Make sure you cannot update a comment on a node to one that already exists
    update = client_valid_access_token.patch(create2.headers["Content-Location"], json={"value": create_json["value"]})
    assert update.status_code == status.HTTP_409_CONFLICT


#
# VALID TESTS
#


def test_update(client_valid_access_token):
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

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"value": "updated"})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read the node back to make sure it shows the updated comment
    get_node = client_valid_access_token.get(node_create.headers["Content-Location"])
    assert get_node.json()["comments"][0]["value"] == "updated"
