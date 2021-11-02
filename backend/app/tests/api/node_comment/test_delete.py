import uuid

from fastapi import status

from tests import helpers


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


def test_delete(client_valid_access_token, db):
    # Create a node
    node = helpers.create_analysis(db=db)

    # Create a comment
    comment = helpers.create_node_comment(node=node, username="johndoe", value="test", db=db)
    assert len(node.comments) == 1

    # Delete it
    delete = client_valid_access_token.delete(f"/api/node/comment/{comment.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(f"/api/node/comment/{comment.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the comment
    assert len(node.comments) == 0
