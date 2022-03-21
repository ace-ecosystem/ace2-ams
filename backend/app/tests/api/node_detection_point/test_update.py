import pytest
import uuid

from fastapi import status

from tests import helpers


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
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/node/detection_point/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/node/detection_point/1", json={"value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/node/detection_point/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_duplicate_node_uuid_value(client_valid_access_token, db):
    # Create an observable
    node_tree = helpers.create_alert(db=db)
    observable = helpers.create_observable(type="test_type", value="test_value", parent_tree=node_tree, db=db)

    # Create some detection points
    detection_point1 = helpers.create_node_detection_point(
        node=observable.node, username="analyst", value="test", db=db
    )
    detection_point2 = helpers.create_node_detection_point(
        node=observable.node, username="analyst", value="test2", db=db
    )

    # Make sure you cannot update a detection point on a node to one that already exists
    update = client_valid_access_token.patch(
        f"/api/node/detection_point/{detection_point2.uuid}", json={"value": detection_point1.value}
    )
    assert update.status_code == status.HTTP_409_CONFLICT


#
# VALID TESTS
#


def test_update_observables(client_valid_access_token, db):
    # Create a detection point
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test_value", parent_tree=alert_tree, db=db)
    detection_point = helpers.create_node_detection_point(
        node=observable_tree.node, username="analyst", value="test", db=db
    )
    original_time = detection_point.insert_time
    assert observable_tree.node.detection_points[0].value == "test"

    # Update it
    update = client_valid_access_token.patch(
        f"/api/node/detection_point/{detection_point.uuid}", json={"value": "updated"}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert observable_tree.node.detection_points[0].value == "updated"
    assert observable_tree.node.detection_points[0].insert_time != original_time

    # Verify the history record
    history = client_valid_access_token.get(f"/api/observable/{observable_tree.node_uuid}/history")

    assert history.json()["total"] == 3
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(observable_tree.node_uuid)
    assert history.json()["items"][1]["field"] == "detection_points"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] is None
    assert history.json()["items"][1]["snapshot"]["value"] == "test_value"

    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(observable_tree.node_uuid)
    assert history.json()["items"][2]["field"] == "detection_points"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == ["updated"]
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["value"] == "test_value"
