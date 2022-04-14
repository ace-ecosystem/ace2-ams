import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/analysis/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/analysis/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get(client, db):
    alert_tree = helpers.create_alert(db=db)
    analysis_tree = helpers.create_analysis(parent_tree=alert_tree, db=db)

    get = client.get(f"/api/analysis/{analysis_tree.node.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["node_type"] == "analysis"
