import pytest
import uuid

from dateutil.parser import parse
from fastapi import status

from db import crud
from tests.api.node import INVALID_LIST_STRING_VALUES, VALID_LIST_STRING_VALUES
from tests import factory


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", 123),
        ("description", ""),
        ("disposition", 123),
        ("disposition", ""),
        ("event_uuid", 123),
        ("event_uuid", ""),
        ("event_uuid", "abc"),
        ("event_time", None),
        ("event_time", ""),
        ("event_time", "Monday"),
        ("event_time", "2022-01-01"),
        ("instructions", 123),
        ("instructions", ""),
        ("owner", 123),
        ("owner", ""),
        ("queue", 123),
        ("queue", None),
        ("queue", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.patch("/api/alert/", json=[{key: value, "uuid": str(uuid.uuid4())}])
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,values",
    [
        ("tags", INVALID_LIST_STRING_VALUES),
        ("threat_actors", INVALID_LIST_STRING_VALUES),
        ("threats", INVALID_LIST_STRING_VALUES),
    ],
)
def test_update_invalid_node_fields(client, key, values):
    for value in values:
        update = client.patch("/api/alert/", json=[{key: value, "uuid": str(uuid.uuid4())}])
        assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in update.json()["detail"][0]["loc"]


def test_update_invalid_uuid(client):
    update = client.patch("/api/alert/", json=[{"uuid": "1"}])
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client, db):
    alert = factory.alert.create(db=db)

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client.patch("/api/alert/", json=[{"version": str(uuid.uuid4()), "uuid": str(alert.uuid)}])
    assert update.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "key,value",
    [
        ("disposition", "abc"),
        ("event_uuid", str(uuid.uuid4())),
        ("owner", "johndoe"),
        ("queue", "abc"),
    ],
)
def test_update_nonexistent_fields(client, db, key, value):
    alert = factory.alert.create(db=db)

    # Make sure you cannot update it to use a nonexistent field value
    update = client.patch("/api/alert/", json=[{key: value, "uuid": str(alert.uuid), "history_username": "analyst"}])
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key",
    [("tags"), ("threat_actors"), ("threats")],
)
def test_update_nonexistent_node_fields(client, db, key):
    alert = factory.alert.create(db=db)

    # Make sure you cannot update it to use a nonexistent node field value
    update = client.patch("/api/alert/", json=[{key: ["abc"], "uuid": str(alert.uuid)}])
    assert update.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in update.text


def test_update_nonexistent_uuid(client):
    update = client.patch("/api/alert/", json=[{"uuid": str(uuid.uuid4())}])
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_disposition(client, db):
    alert = factory.alert.create(db=db, history_username="analyst")
    initial_version = alert.version

    # Create a user
    factory.user.create_or_read(username="analyst", db=db)

    # Create a disposition
    factory.alert_disposition.create_or_read(value="test", rank=1, db=db)

    # Update the disposition
    update = client.patch(
        "/api/alert/", json=[{"disposition": "test", "uuid": str(alert.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.disposition.value == "test"
    assert alert.version != initial_version

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "disposition"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "test"
    assert history.json()["items"][1]["snapshot"]["disposition"]["value"] == "test"

    # Set it back to None
    update = client.patch(
        "/api/alert/", json=[{"disposition": None, "uuid": str(alert.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.disposition is None

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "disposition"
    assert history.json()["items"][2]["diff"]["old_value"] == "test"
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["disposition"] is None


def test_update_event_uuid(client, db):
    alert = factory.alert.create(db=db, history_username="analyst")
    initial_alert_version = alert.version

    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Update the alert to add it to the event
    update = client.patch(
        "/api/alert/",
        json=[{"event_uuid": str(event.uuid), "uuid": str(alert.uuid), "history_username": "analyst"}],
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.event_uuid == event.uuid
    assert alert.version != initial_alert_version

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "event_uuid"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == str(event.uuid)
    assert history.json()["items"][1]["snapshot"]["event_uuid"] == str(event.uuid)

    # By adding the alert to the event, you should be able to see the alert UUID in the event's
    # alert_uuids list even though it was not explicitly added.
    # event = crud.event.read_by_uuid(uuid=event.uuid, db=db)
    assert event.alert_uuids == [alert.uuid]

    # Additionally, adding the alert to the event should trigger the event to have a new version.
    assert event.version != initial_event_version

    # Set it back to None
    update = client.patch(
        "/api/alert/", json=[{"event_uuid": None, "uuid": str(alert.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.event is None

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "event_uuid"
    assert history.json()["items"][2]["diff"]["old_value"] == str(event.uuid)
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["event_uuid"] is None


def test_update_owner(client, db):
    alert = factory.alert.create(db=db, history_username="analyst")
    initial_alert_version = alert.version

    # Create a user
    factory.user.create_or_read(username="johndoe", db=db)

    # Update the owner
    update = client.patch(
        "/api/alert/", json=[{"owner": "johndoe", "uuid": str(alert.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.owner.username == "johndoe"
    assert alert.version != initial_alert_version

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "owner"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "johndoe"
    assert history.json()["items"][1]["snapshot"]["owner"]["username"] == "johndoe"

    # Set it back to None
    update = client.patch("/api/alert/", json=[{"owner": None, "uuid": str(alert.uuid), "history_username": "analyst"}])
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.owner is None

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "owner"
    assert history.json()["items"][2]["diff"]["old_value"] == "johndoe"
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["owner"] is None


def test_update_queue(client, db):
    alert = factory.alert.create(alert_queue="external", db=db, history_username="analyst")
    initial_alert_version = alert.version

    # Create a new alert queue
    factory.queue.create_or_read(value="updated_queue", db=db)

    # Update the queue
    update = client.patch(
        "/api/alert/", json=[{"queue": "updated_queue", "uuid": str(alert.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.queue.value == "updated_queue"
    assert alert.version != initial_alert_version

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "queue"
    assert history.json()["items"][1]["diff"]["old_value"] == "external"
    assert history.json()["items"][1]["diff"]["new_value"] == "updated_queue"
    assert history.json()["items"][1]["snapshot"]["queue"]["value"] == "updated_queue"


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("tags", VALID_LIST_STRING_VALUES, factory.node_tag.create_or_read),
        ("threat_actors", VALID_LIST_STRING_VALUES, factory.node_threat_actor.create_or_read),
        ("threats", VALID_LIST_STRING_VALUES, factory.node_threat.create_or_read),
    ],
)
def test_update_valid_node_fields(client, db, key, value_lists, helper_create_func):
    for value_list in value_lists:
        alert = factory.alert.create(
            tags=["remove_me"],
            threat_actors=["remove_me"],
            threats=["remove_me"],
            db=db,
            history_username="analyst",
        )
        initial_alert_version = alert.version

        for value in value_list:
            helper_create_func(value=value, db=db)

        # helpers.create_queue(value="test_queue", db=db)
        # factory.alert.create_type(value="test_type", db=db)
        # helpers.create_observable_type(value="o_type", db=db)

        # Update the alert
        update = client.patch(
            "/api/alert/", json=[{key: value_list, "uuid": str(alert.uuid), "history_username": "analyst"}]
        )
        assert update.status_code == status.HTTP_204_NO_CONTENT
        assert len(getattr(alert, key)) == len(set(value_list))
        assert alert.version != initial_alert_version

        # Verify the history
        if value_list:
            history = client.get(f"/api/alert/{alert.uuid}/history")
            assert history.json()["total"] == 2
            assert history.json()["items"][1]["action"] == "UPDATE"
            assert history.json()["items"][1]["action_by"]["username"] == "analyst"
            assert history.json()["items"][1]["field"] == key
            assert history.json()["items"][1]["diff"]["old_value"] is None
            assert history.json()["items"][1]["diff"]["new_value"] is None
            assert history.json()["items"][1]["diff"]["added_to_list"] == sorted(set(value_list))
            assert history.json()["items"][1]["diff"]["removed_from_list"] == ["remove_me"]
            assert len(history.json()["items"][1]["snapshot"][key]) == len(set(value_list))


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", None),
        ("description", "test", "test"),
        ("event_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00+00:00"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000+00:00"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("instructions", None, "test"),
        ("instructions", "test", None),
        ("instructions", "test", "test"),
    ],
)
def test_update(client, db, key, initial_value, updated_value):
    alert = factory.alert.create(db=db, history_username="analyst")
    initial_alert_version = alert.version

    # Set the initial value on the alert
    setattr(alert, key, initial_value)
    assert getattr(alert, key) == initial_value

    # Update it
    update = client.patch(
        "/api/alert/", json=[{key: updated_value, "uuid": str(alert.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == key
    assert history.json()["items"][1]["diff"]["old_value"] == initial_value

    if key == "event_time":
        assert alert.event_time == parse("2022-01-01T00:00:00+00:00")
        assert history.json()["items"][1]["diff"]["new_value"] == parse("2022-01-01T00:00:00+00:00").isoformat()
    else:
        assert getattr(alert, key) == updated_value
        assert history.json()["items"][1]["diff"]["new_value"] == updated_value
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"

    assert alert.version != initial_alert_version


def test_update_multiple_alerts(client, db):
    alert1 = factory.alert.create(db=db, history_username="analyst")
    initial_alert1_version = alert1.version

    alert2 = factory.alert.create(db=db, history_username="analyst")
    initial_alert2_version = alert2.version
    initial_event_time = alert2.event_time.isoformat()

    alert3 = factory.alert.create(db=db, history_username="analyst")
    initial_alert3_version = alert3.version

    assert alert1.description is None
    assert alert2.event_time != parse("2022-01-01T00:00:00+00:00")
    assert alert3.instructions is None

    # Update all the alerts at once
    update_data = [
        {"description": "updated_description", "uuid": str(alert1.uuid), "history_username": "analyst"},
        {"event_time": "2022-01-01 00:00:00+00:00", "uuid": str(alert2.uuid), "history_username": "analyst"},
        {"instructions": "updated_instructions", "uuid": str(alert3.uuid), "history_username": "analyst"},
    ]
    update = client.patch("/api/alert/", json=update_data)
    assert update.status_code == status.HTTP_204_NO_CONTENT

    assert alert1.description == "updated_description"
    assert alert1.version != initial_alert1_version

    assert alert2.event_time == parse("2022-01-01T00:00:00+00:00")
    assert alert2.version != initial_alert2_version

    assert alert3.instructions == "updated_instructions"
    assert alert3.version != initial_alert3_version

    # Verify the history
    history = client.get(f"/api/alert/{alert1.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "description"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "updated_description"
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"

    history = client.get(f"/api/alert/{alert2.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "event_time"
    assert history.json()["items"][1]["diff"]["old_value"] == initial_event_time
    assert history.json()["items"][1]["diff"]["new_value"] == parse("2022-01-01T00:00:00+00:00").isoformat()
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"

    history = client.get(f"/api/alert/{alert3.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "instructions"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "updated_instructions"
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"


def test_update_multiple_fields(client, db):
    alert = factory.alert.create(db=db, history_username="analyst")
    initial_alert_version = alert.version

    # Update it
    update = client.patch(
        "/api/alert/",
        json=[
            {
                "description": "updated_description",
                "history_username": "analyst",
                "instructions": "updated_instructions",
                "uuid": str(alert.uuid),
            }
        ],
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.version != initial_alert_version

    # Verify the history
    history = client.get(f"/api/alert/{alert.uuid}/history")
    print(history.json())
    assert history.json()["total"] == 3
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "description"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "updated_description"
    assert history.json()["items"][1]["snapshot"]["description"] == "updated_description"
    assert history.json()["items"][1]["snapshot"]["instructions"] == "updated_instructions"

    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "instructions"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] == "updated_instructions"
    assert history.json()["items"][2]["snapshot"]["description"] == "updated_description"
    assert history.json()["items"][2]["snapshot"]["instructions"] == "updated_instructions"
