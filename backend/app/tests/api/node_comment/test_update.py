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
    update = client_valid_access_token.patch(f"/api/node/comment/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/node/comment/1", json={"value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/node/comment/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_duplicate_node_uuid_value(client_valid_access_token, db):
    # Create a node
    node_tree = helpers.create_alert(db=db)

    # Create some comments
    comment1 = helpers.create_node_comment(node=node_tree.node, username="johndoe", value="test", db=db)
    comment2 = helpers.create_node_comment(node=node_tree.node, username="johndoe", value="test2", db=db)

    # Make sure you cannot update a comment on a node to one that already exists
    update = client_valid_access_token.patch(f"/api/node/comment/{comment2.uuid}", json={"value": comment1.value})
    assert update.status_code == status.HTTP_409_CONFLICT


#
# VALID TESTS
#


def test_update_alerts(client_valid_access_token, db):
    # Create a comment
    alert_tree = helpers.create_alert(db=db)
    comment = helpers.create_node_comment(node=alert_tree.node, username="johndoe", value="test", db=db)
    assert alert_tree.node.comments[0].value == "test"

    # Update it
    update = client_valid_access_token.patch(f"/api/node/comment/{comment.uuid}", json={"value": "updated"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert_tree.node.comments[0].value == "updated"

    # Verify the history record
    history = client_valid_access_token.get(f"/api/alert/{alert_tree.node_uuid}/history")
    assert history.json()["total"] == 1
    assert history.json()["items"][0]["action"] == "UPDATE"
    assert history.json()["items"][0]["action_by"] == "analyst"
    assert history.json()["items"][0]["record_uuid"] == str(alert_tree.node_uuid)
    assert history.json()["items"][0]["field"] == "comments"
    assert history.json()["items"][0]["diff"]["old_value"] is None
    assert history.json()["items"][0]["diff"]["new_value"] is None
    assert history.json()["items"][0]["diff"]["added_to_list"] == ["updated"]
    assert history.json()["items"][0]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][0]["snapshot"]["name"] == "Test Alert"


def test_update_events(client_valid_access_token, db):
    # Create a comment
    event = helpers.create_event(name="Test Event", db=db)
    comment = helpers.create_node_comment(node=event, username="johndoe", value="test", db=db)
    assert event.comments[0].value == "test"

    # Update it
    update = client_valid_access_token.patch(f"/api/node/comment/{comment.uuid}", json={"value": "updated"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.comments[0].value == "updated"

    # Verify the history record
    history = client_valid_access_token.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 1
    assert history.json()["items"][0]["action"] == "UPDATE"
    assert history.json()["items"][0]["action_by"] == "analyst"
    assert history.json()["items"][0]["record_uuid"] == str(event.uuid)
    assert history.json()["items"][0]["field"] == "comments"
    assert history.json()["items"][0]["diff"]["old_value"] is None
    assert history.json()["items"][0]["diff"]["new_value"] is None
    assert history.json()["items"][0]["diff"]["added_to_list"] == ["updated"]
    assert history.json()["items"][0]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][0]["snapshot"]["name"] == "Test Event"


def test_update_observables(client_valid_access_token, db):
    # Create a comment
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test_value", parent_tree=alert_tree, db=db)
    comment = helpers.create_node_comment(node=observable_tree.node, username="johndoe", value="test", db=db)
    assert observable_tree.node.comments[0].value == "test"

    # Update it
    update = client_valid_access_token.patch(f"/api/node/comment/{comment.uuid}", json={"value": "updated"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert observable_tree.node.comments[0].value == "updated"

    # Verify the history record
    history = client_valid_access_token.get(f"/api/observable/{observable_tree.node_uuid}/history")
    assert history.json()["total"] == 1
    assert history.json()["items"][0]["action"] == "UPDATE"
    assert history.json()["items"][0]["action_by"] == "analyst"
    assert history.json()["items"][0]["record_uuid"] == str(observable_tree.node_uuid)
    assert history.json()["items"][0]["field"] == "comments"
    assert history.json()["items"][0]["diff"]["old_value"] is None
    assert history.json()["items"][0]["diff"]["new_value"] is None
    assert history.json()["items"][0]["diff"]["added_to_list"] == ["updated"]
    assert history.json()["items"][0]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][0]["snapshot"]["value"] == "test_value"
