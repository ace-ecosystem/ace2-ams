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


def test_update_duplicate_node_uuid_value(client_valid_access_token, db):
    # Create a node
    node = helpers.create_alert(db=db)

    # Create some comments
    comment1 = helpers.create_node_comment(node=node, username="johndoe", value="test", db=db)
    comment2 = helpers.create_node_comment(node=node, username="johndoe", value="test2", db=db)

    # Make sure you cannot update a comment on a node to one that already exists
    update = client_valid_access_token.patch(f"/api/node/comment/{comment2.uuid}", json={"value": comment1.value})
    assert update.status_code == status.HTTP_409_CONFLICT


#
# VALID TESTS
#


def test_update(client_valid_access_token, db):
    # Create a node
    node = helpers.create_alert(db=db)

    # Create a comment
    comment = helpers.create_node_comment(node=node, username="johndoe", value="test", db=db)
    assert node.comments[0].value == "test"

    # Update it
    update = client_valid_access_token.patch(f"/api/node/comment/{comment.uuid}", json={"value": "updated"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert node.comments[0].value == "updated"
