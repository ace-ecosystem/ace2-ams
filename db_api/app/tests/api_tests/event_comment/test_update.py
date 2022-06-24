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
    update = client.patch(f"/api/event/comment/{uuid.uuid4()}", json={key: value, "username": "analyst"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client):
    update = client.patch("/api/event/comment/1", json={"value": "test", "username": "analyst"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_event_uuid_value(client, db):
    event = factory.event.create_or_read(name="Test Event", db=db, history_username="analyst")

    # Create some comments
    comment1 = factory.event_comment.create_or_read(event=event, username="johndoe", value="test", db=db)
    comment2 = factory.event_comment.create_or_read(event=event, username="johndoe", value="test2", db=db)

    # Make sure you cannot update a comment on a event to one that already exists
    update = client.patch(f"/api/event/comment/{comment2.uuid}", json={"value": comment1.value, "username": "johndoe"})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/event/comment/{uuid.uuid4()}", json={"value": "test", "username": "analyst"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_events(client, db):
    # Create a comment
    event = factory.event.create_or_read(name="Test Event", db=db, history_username="analyst")
    comment = factory.event_comment.create_or_read(event=event, username="johndoe", value="test", db=db)
    original_time = comment.insert_time
    assert event.comments[0].value == "test"
    assert comment.user.username == "johndoe"

    # Update it
    update = client.patch(f"/api/event/comment/{comment.uuid}", json={"value": "updated", "username": "analyst"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.comments[0].value == "updated"
    assert event.comments[0].user.username == "analyst"
    assert event.comments[0].insert_time != original_time

    # Verify the history record
    history = client.get(f"/api/event/{event.uuid}/history")

    assert history.json()["total"] == 3
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "johndoe"
    assert history.json()["items"][1]["record_uuid"] == str(event.uuid)
    assert history.json()["items"][1]["field"] == "comments"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Event"

    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(event.uuid)
    assert history.json()["items"][2]["field"] == "comments"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == ["updated"]
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["name"] == "Test Event"
