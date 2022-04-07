import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_version_invalid_uuid(client):
    get = client.get("/api/node/1/version")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_version_nonexistent_uuid(client):
    get = client.get(f"/api/node/{uuid.uuid4()}/version")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_version(client, db):
    alert_tree = helpers.create_alert(db=db)
    analysis_tree = helpers.create_analysis(parent_tree=alert_tree, db=db)

    get = client.get(f"/api/node/{analysis_tree.node_uuid}/version")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {"version": str(analysis_tree.node.version)}
