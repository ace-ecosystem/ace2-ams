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
    delete = client_valid_access_token.delete("/api/user/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete(f"/api/user/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client_valid_access_token, db):
    # Create an alert queue
    alert_queue = helpers.create_alert_queue(value="test_queue", db=db)

    # Create a user role
    user_role = helpers.create_user_role(value="test_role", db=db)

    # Create a user
    user = helpers.create_user(username="johndoe", alert_queue="test_queue", roles=["test_role"], db=db)

    # Read it back
    get = client_valid_access_token.get(f"/api/user/{user.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client_valid_access_token.delete(f"/api/user/{user.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(f"/api/user/{user.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the alert queue is still there
    get = client_valid_access_token.get(f"/api/alert/queue/{alert_queue.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Make sure the user role is still there
    get = client_valid_access_token.get(f"/api/user/role/{user_role.uuid}")
    assert get.status_code == status.HTTP_200_OK
