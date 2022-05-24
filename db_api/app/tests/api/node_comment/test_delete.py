import uuid

from fastapi import status

from tests import factory


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/node/comment/1?history_username=analyst")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/node/comment/{uuid.uuid4()}?history_username=analyst")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete_alerts(client, db):
    # Create a comment
    alert = factory.alert.create(db=db, history_username="analyst")
    comment = factory.node_comment.create_or_read(node=alert, username="analyst", value="test", db=db)
    assert alert.comments[0].value == "test"

    # Delete it
    delete = client.delete(f"/api/node/comment/{comment.uuid}?history_username=analyst")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/node/comment/{comment.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the comment
    assert len(alert.comments) == 0

    # Verify the history record
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(alert.uuid)
    assert history.json()["items"][2]["field"] == "comments"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == []
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["name"] == "Test Alert"


def test_delete_events(client, db):
    # Create a comment
    event = factory.event.create_or_read(name="Test Event", db=db, history_username="analyst")
    comment = factory.node_comment.create_or_read(node=event, username="analyst", value="test", db=db)
    assert event.comments[0].value == "test"

    # Delete it
    delete = client.delete(f"/api/node/comment/{comment.uuid}?history_username=analyst")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/node/comment/{comment.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the comment
    assert len(event.comments) == 0

    # Verify the history record
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(event.uuid)
    assert history.json()["items"][2]["field"] == "comments"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == []
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["name"] == "Test Event"


def test_delete_observables(client, db):
    # Create a comment
    alert = factory.alert.create(db=db, history_username="analyst")
    observable = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    comment = factory.node_comment.create_or_read(node=observable, username="analyst", value="test", db=db)
    assert observable.comments[0].value == "test"

    # Delete it
    delete = client.delete(f"/api/node/comment/{comment.uuid}?history_username=analyst")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/node/comment/{comment.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the node no longer shows the comment
    assert len(observable.comments) == 0

    # Verify the history record
    history = client.get(f"/api/observable/{observable.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(observable.uuid)
    assert history.json()["items"][2]["field"] == "comments"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == []
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["value"] == "test_value"
