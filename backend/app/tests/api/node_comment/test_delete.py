import uuid

from fastapi import status

from db import crud
from db.schemas.alert import AlertHistory
from db.schemas.event import EventHistory
from db.schemas.history import History
from db.schemas.observable import ObservableHistory
from tests import helpers


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete("/api/node/comment/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete(f"/api/node/comment/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete_alerts(client_valid_access_token, db):
    # Create a comment
    alert_tree = helpers.create_alert(db=db)
    comment = helpers.create_node_comment(node=alert_tree.node, username="johndoe", value="test", db=db)
    assert alert_tree.node.comments[0].value == "test"

    # Delete it
    delete = client_valid_access_token.delete(f"/api/node/comment/{comment.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(f"/api/node/comment/{comment.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the comment
    assert len(alert_tree.node.comments) == 0

    # Verify the history record
    history: list[History] = crud.read_history_records(AlertHistory, record_uuid=alert_tree.node_uuid, db=db)
    assert len(history) == 1
    assert history[0].action == "UPDATE"
    assert history[0].action_by == "analyst"
    assert history[0].record_uuid == alert_tree.node_uuid
    assert history[0].field == "comments"
    assert history[0].diff["old_value"] is None
    assert history[0].diff["new_value"] is None
    assert history[0].diff["added_to_list"] is None
    assert history[0].diff["removed_from_list"] == ["test"]
    assert history[0].snapshot["name"] == "Test Alert"


def test_delete_events(client_valid_access_token, db):
    # Create a comment
    event = helpers.create_event(name="Test Event", db=db)
    comment = helpers.create_node_comment(node=event, username="johndoe", value="test", db=db)
    assert event.comments[0].value == "test"

    # Delete it
    delete = client_valid_access_token.delete(f"/api/node/comment/{comment.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(f"/api/node/comment/{comment.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the comment
    assert len(event.comments) == 0

    # Verify the history record
    history: list[History] = crud.read_history_records(EventHistory, record_uuid=event.uuid, db=db)
    assert len(history) == 1
    assert history[0].action == "UPDATE"
    assert history[0].action_by == "analyst"
    assert history[0].record_uuid == event.uuid
    assert history[0].field == "comments"
    assert history[0].diff["old_value"] is None
    assert history[0].diff["new_value"] is None
    assert history[0].diff["added_to_list"] is None
    assert history[0].diff["removed_from_list"] == ["test"]
    assert history[0].snapshot["name"] == "Test Event"


def test_delete_observables(client_valid_access_token, db):
    # Create a comment
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test_value", parent_tree=alert_tree, db=db)
    comment = helpers.create_node_comment(node=observable_tree.node, username="johndoe", value="test", db=db)
    assert observable_tree.node.comments[0].value == "test"

    # Delete it
    delete = client_valid_access_token.delete(f"/api/node/comment/{comment.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(f"/api/node/comment/{comment.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the comment
    assert len(alert_tree.node.comments) == 0

    # Verify the history record
    history: list[History] = crud.read_history_records(ObservableHistory, record_uuid=observable_tree.node_uuid, db=db)
    assert len(history) == 1
    assert history[0].action == "UPDATE"
    assert history[0].action_by == "analyst"
    assert history[0].record_uuid == observable_tree.node_uuid
    assert history[0].field == "comments"
    assert history[0].diff["old_value"] is None
    assert history[0].diff["new_value"] is None
    assert history[0].diff["added_to_list"] is None
    assert history[0].diff["removed_from_list"] == ["test"]
    assert history[0].snapshot["value"] == "test_value"
