import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete("/api/node/comment/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete(f"/api/node/comment/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client_valid_access_token):
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

    # Delete it
    delete = client_valid_access_token.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the comment
    get_node = client_valid_access_token.get(node_create.headers["Content-Location"])
    assert get_node.json()["comments"] == []
