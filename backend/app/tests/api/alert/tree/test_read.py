import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client_valid_access_token):
    get = client_valid_access_token.get("/api/alert/1/tree")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client_valid_access_token):
    get = client_valid_access_token.get(f"/api/alert/{uuid.uuid4()}/tree")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_alert_tree(client_valid_access_token, db):
    # Create an alert with a tree of analyses and observable instances
    alert = helpers.create_realistic_alert(db)

    get = client_valid_access_token.get(f"/api/alert/{alert.uuid}/tree")
    assert len(get.json()["analyses"]) == 7
    assert len(get.json()["observable_instances"]) == 12
