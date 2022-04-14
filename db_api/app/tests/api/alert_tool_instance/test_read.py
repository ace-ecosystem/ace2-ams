import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/alert/tool/instance/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/alert/tool/instance/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client, db):
    # Create some objects
    helpers.create_alert_tool_instance(value="test", db=db)
    helpers.create_alert_tool_instance(value="test2", db=db)

    # Read them back
    get = client.get("/api/alert/tool/instance/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 2


def test_get_all_empty(client):
    get = client.get("/api/alert/tool/instance/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 0
