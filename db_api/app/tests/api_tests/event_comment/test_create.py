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
        ("event_uuid", 123),
        ("event_uuid", None),
        ("event_uuid", ""),
        ("event_uuid", "abc"),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client, key, value):
    create = client.post("/api/event/comment/", json=[{key: value, "username": "analyst"}])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_event_uuid(client):
    # Create a comment
    create_json = {
        "event_uuid": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "value": "test",
        "username": "analyst",
    }
    create = client.post("/api/event/comment/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_create_verify_history_events(client, db):
    event = factory.event.create_or_read(name="test event", db=db, history_username="analyst")

    # Add a comment to the event
    create_json = [
        {"event_uuid": str(event.uuid), "value": "test", "username": "analyst"},
    ]
    create = client.post("/api/event/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(event.uuid)
    assert history.json()["items"][1]["field"] == "comments"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["name"] == "test event"


def test_create_multiple(client, db):
    event1 = factory.event.create_or_read(name="test event1", db=db, history_username="analyst")
    initial_event1_version = event1.version

    event2 = factory.event.create_or_read(name="test event2", db=db, history_username="analyst")
    initial_event2_version = event2.version

    event3 = factory.event.create_or_read(name="test event3", db=db, history_username="analyst")
    initial_event3_version = event3.version

    assert event1.comments == []
    assert event2.comments == []
    assert event3.comments == []

    # Add a comment to each event at once
    create_json = [
        {"event_uuid": str(event1.uuid), "value": "test1", "username": "analyst"},
        {"event_uuid": str(event2.uuid), "value": "test2", "username": "analyst"},
        {"event_uuid": str(event3.uuid), "value": "test3", "username": "analyst"},
    ]
    create = client.post("/api/event/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    assert len(event1.comments) == 1
    assert event1.comments[0].value == "test1"
    assert event1.comments[0].user.username == "analyst"
    assert event1.version != initial_event1_version

    assert len(event2.comments) == 1
    assert event2.comments[0].value == "test2"
    assert event2.comments[0].user.username == "analyst"
    assert event2.version != initial_event2_version

    assert len(event3.comments) == 1
    assert event3.comments[0].value == "test3"
    assert event3.comments[0].user.username == "analyst"
    assert event3.version != initial_event3_version


def test_create_valid_required_fields(client, db):
    event = factory.event.create_or_read(name="test event", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create a comment
    create_json = {
        "event_uuid": str(event.uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test",
        "username": "analyst",
    }
    create = client.post("/api/event/comment/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED
    assert len(event.comments) == 1
    assert event.comments[0].value == "test"
    assert event.comments[0].user.username == "analyst"
    assert event.version != initial_event_version
