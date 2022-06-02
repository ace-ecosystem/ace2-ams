import pytest
import uuid

from fastapi import status

from tests import factory


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
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/node/detection_point/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client):
    update = client.patch("/api/node/detection_point/1", json={"value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_node_uuid_value(client, db):
    alert = factory.submission.create(db=db, history_username="analyst")
    observable = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )

    # Create some detection points
    detection_point1 = factory.node_detection_point.create_or_read(node=observable, value="test", db=db)
    detection_point2 = factory.node_detection_point.create_or_read(node=observable, value="test2", db=db)

    # Make sure you cannot update a detection point on a node to one that already exists
    update = client.patch(f"/api/node/detection_point/{detection_point2.uuid}", json={"value": detection_point1.value})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/node/detection_point/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_observables(client, db):
    # Create a detection point
    alert = factory.submission.create(db=db, history_username="analyst")
    observable = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    detection_point = factory.node_detection_point.create_or_read(
        node=observable, value="test", db=db, history_username="analyst"
    )
    original_time = detection_point.insert_time
    assert observable.detection_points[0].value == "test"

    # Update it
    update = client.patch(
        f"/api/node/detection_point/{detection_point.uuid}", json={"value": "updated", "history_username": "analyst"}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert observable.detection_points[0].value == "updated"
    assert observable.detection_points[0].insert_time != original_time

    # Verify the history record
    history = client.get(f"/api/observable/{observable.uuid}/history")

    assert history.json()["total"] == 3
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(observable.uuid)
    assert history.json()["items"][1]["field"] == "detection_points"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["value"] == "test_value"

    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(observable.uuid)
    assert history.json()["items"][2]["field"] == "detection_points"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == ["updated"]
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["value"] == "test_value"
