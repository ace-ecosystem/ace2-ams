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
    delete = client_valid_access_token.delete("/api/observable/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete(f"/api/observable/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client_valid_access_token, db):
    # Create an observable type
    observable_type = helpers.create_observable_type(value="test_type", db=db)

    # Create the observable
    observable = helpers.create_observable(type="test_type", value="test", db=db)

    # Read it back
    get = client_valid_access_token.get(f"/api/observable/{observable.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client_valid_access_token.delete(f"/api/observable/{observable.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(f"/api/observable/{observable.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the observable type is still there
    get = client_valid_access_token.get(f"/api/observable/type/{observable_type.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_type"
