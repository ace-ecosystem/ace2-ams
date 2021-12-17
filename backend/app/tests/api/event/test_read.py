import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client_valid_access_token):
    get = client_valid_access_token.get("/api/event/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client_valid_access_token):
    get = client_valid_access_token.get(f"/api/event/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get(client_valid_access_token, db):
    event = helpers.create_event(name="Test Event", db=db)

    get = client_valid_access_token.get(f"/api/event/{event.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["node_type"] == "event"
