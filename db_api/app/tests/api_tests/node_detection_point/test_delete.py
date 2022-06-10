import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/node/detection_point/1?history_username=analyst")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/node/detection_point/{uuid.uuid4()}?history_username=analyst")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client, db):
    # Create a detection point
    alert = factory.submission.create(db=db, history_username="analyst")
    observable = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    detection_point = factory.node_detection_point.create_or_read(
        node=observable, value="test", db=db, history_username="analyst"
    )
    assert observable.detection_points[0].value == "test"

    # Delete it
    delete = client.delete(f"/api/node/detection_point/{detection_point.uuid}?history_username=analyst")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/node/detection_point/{detection_point.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the detection point
    assert len(observable.detection_points) == 0

    # Verify the history record
    history = client.get(f"/api/observable/{observable.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(observable.uuid)
    assert history.json()["items"][2]["field"] == "detection_points"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == []
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["detection_points"] == []
