import pytest
import uuid

from dateutil.parser import parse
from fastapi import status

from tests.api_tests.node import INVALID_LIST_STRING_VALUES, VALID_LIST_STRING_VALUES
from tests import factory


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("alert_time", ""),
        ("alert_time", "Monday"),
        ("alert_time", "2022-01-01"),
        ("contain_time", ""),
        ("contain_time", "Monday"),
        ("contain_time", "2022-01-01"),
        ("disposition_time", ""),
        ("disposition_time", "Monday"),
        ("disposition_time", "2022-01-01"),
        ("event_time", ""),
        ("event_time", "Monday"),
        ("event_time", "2022-01-01"),
        ("name", 123),
        ("name", None),
        ("name", ""),
        ("owner", 123),
        ("owner", ""),
        ("ownership_time", ""),
        ("ownership_time", "Monday"),
        ("ownership_time", "2022-01-01"),
        ("prevention_tools", None),
        ("prevention_tools", "test_type"),
        ("prevention_tools", [123]),
        ("prevention_tools", [None]),
        ("prevention_tools", [""]),
        ("prevention_tools", ["abc", 123]),
        ("queue", 123),
        ("queue", None),
        ("queue", ""),
        ("remediation_time", ""),
        ("remediation_time", "Monday"),
        ("remediation_time", "2022-01-01"),
        ("remediations", None),
        ("remediations", "test_type"),
        ("remediations", [123]),
        ("remediations", [None]),
        ("remediations", [""]),
        ("remediations", ["abc", 123]),
        ("severity", 123),
        ("severity", ""),
        ("source", 123),
        ("source", ""),
        ("status", 123),
        ("status", None),
        ("status", ""),
        ("type", 123),
        ("type", ""),
        ("vectors", None),
        ("vectors", "test_type"),
        ("vectors", [123]),
        ("vectors", [None]),
        ("vectors", [""]),
        ("vectors", ["abc", 123]),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.patch("/api/event/", json=[{key: value, "uuid": str(uuid.uuid4())}])
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
        update = client.patch("/api/event/", json=[{key: value, "uuid": str(uuid.uuid4())}])
        assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in update.json()["detail"][0]["loc"]


def test_update_invalid_uuid(client):
    update = client.patch("/api/event/", json=[{"uuid": "1"}])
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client, db):
    # create an event
    event = factory.event.create_or_read(name="test", db=db)

    ## Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client.patch("/api/event/", json=[{"version": str(uuid.uuid4()), "uuid": str(event.uuid)}])
    assert update.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "key,value",
    [
        ("owner", "johndoe"),
        ("prevention_tools", ["abc"]),
        ("queue", "abc"),
        ("remediations", ["abc"]),
        ("severity", "abc"),
        ("source", "abc"),
        ("status", "abc"),
        ("type", "abc"),
        ("vectors", ["abc"]),
    ],
)
def test_update_nonexistent_fields(client, db, key, value):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db)

    # Make sure you cannot update it to use a nonexistent field value
    update = client.patch("/api/event/", json=[{key: value, "uuid": str(event.uuid)}])
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key",
    [("tags"), ("threat_actors"), ("threats")],
)
def test_update_nonexistent_node_fields(client, db, key):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db)

    # Make sure you cannot update it to use a nonexistent node field value
    update = client.patch("/api/event/", json=[{key: ["abc"], "uuid": str(event.uuid)}])
    assert update.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in update.text


def test_update_nonexistent_uuid(client):
    update = client.patch("/api/event/", json=[{"uuid": str(uuid.uuid4())}])
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_owner(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create a user
    factory.user.create_or_read(username="johndoe", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"owner": "johndoe", "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.owner.username == "johndoe"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "owner"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "johndoe"
    assert history.json()["items"][1]["snapshot"]["owner"]["username"] == "johndoe"

    # Set it back to None
    update = client.patch("/api/event/", json=[{"owner": None, "uuid": str(event.uuid), "history_username": "analyst"}])
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.owner is None

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "owner"
    assert history.json()["items"][2]["diff"]["old_value"] == "johndoe"
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["owner"] is None


def test_update_prevention_tools(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event prevention tool
    factory.event_prevention_tool.create_or_read(value="test", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"prevention_tools": ["test"], "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(event.prevention_tools) == 1
    assert event.prevention_tools[0].value == "test"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "prevention_tools"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["prevention_tools"][0]["value"] == "test"

    # Set it back to None
    update = client.patch(
        "/api/event/", json=[{"prevention_tools": [], "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.prevention_tools == []

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "prevention_tools"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == []
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["prevention_tools"] == []


def test_update_queue(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", event_queue="external", db=db, history_username="analyst")
    initial_event_version = event.version
    assert event.queue.value == "external"

    # Create an event queue
    factory.queue.create_or_read(value="updated_queue", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"queue": "updated_queue", "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.queue.value == "updated_queue"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "queue"
    assert history.json()["items"][1]["diff"]["old_value"] == "external"
    assert history.json()["items"][1]["diff"]["new_value"] == "updated_queue"
    assert history.json()["items"][1]["snapshot"]["queue"]["value"] == "updated_queue"


def test_update_remediations(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event remediation
    factory.event_remediation.create_or_read(value="test", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"remediations": ["test"], "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(event.remediations) == 1
    assert event.remediations[0].value == "test"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "remediations"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["remediations"][0]["value"] == "test"

    # Set it back to None
    update = client.patch(
        "/api/event/", json=[{"remediations": [], "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.remediations == []

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "remediations"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == []
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["remediations"] == []


def test_update_severity(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event severity
    factory.event_severity.create_or_read(value="test", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"severity": "test", "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.severity.value == "test"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "severity"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "test"
    assert history.json()["items"][1]["snapshot"]["severity"]["value"] == "test"

    # Set it back to None
    update = client.patch(
        "/api/event/", json=[{"severity": None, "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.severity is None

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "severity"
    assert history.json()["items"][2]["diff"]["old_value"] == "test"
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["severity"] is None


def test_update_source(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event source
    factory.event_source.create_or_read(value="test", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"source": "test", "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.source.value == "test"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "source"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "test"
    assert history.json()["items"][1]["snapshot"]["source"]["value"] == "test"

    # Set it back to None
    update = client.patch(
        "/api/event/", json=[{"source": None, "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.source is None

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "source"
    assert history.json()["items"][2]["diff"]["old_value"] == "test"
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["source"] is None


def test_update_status(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event status
    factory.event_status.create_or_read(value="test", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"status": "test", "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.status.value == "test"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "status"
    assert history.json()["items"][1]["diff"]["old_value"] == "OPEN"
    assert history.json()["items"][1]["diff"]["new_value"] == "test"
    assert history.json()["items"][1]["snapshot"]["status"]["value"] == "test"


def test_update_type(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event type
    factory.event_type.create_or_read(value="test", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"type": "test", "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.type.value == "test"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "type"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "test"
    assert history.json()["items"][1]["snapshot"]["type"]["value"] == "test"

    # Set it back to None
    update = client.patch("/api/event/", json=[{"type": None, "uuid": str(event.uuid), "history_username": "analyst"}])
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.type is None

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "type"
    assert history.json()["items"][2]["diff"]["old_value"] == "test"
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["type"] is None


def test_update_vectors(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event vector
    factory.event_vector.create_or_read(value="test", db=db)

    # Update the event
    update = client.patch(
        "/api/event/", json=[{"vectors": ["test"], "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(event.vectors) == 1
    assert event.vectors[0].value == "test"
    assert event.version != initial_event_version

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "vectors"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["vectors"][0]["value"] == "test"

    # Set it back to None
    update = client.patch(
        "/api/event/",
        json=[{"vectors": [], "uuid": str(event.uuid), "uuid": str(event.uuid), "history_username": "analyst"}],
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.vectors == []

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "vectors"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == []
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["vectors"] == []


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("tags", VALID_LIST_STRING_VALUES, factory.tag.create_or_read),
        ("threat_actors", VALID_LIST_STRING_VALUES, factory.node_threat_actor.create_or_read),
        ("threats", VALID_LIST_STRING_VALUES, factory.node_threat.create_or_read),
    ],
)
def test_update_valid_node_fields(client, db, key, value_lists, helper_create_func):
    for value_list in value_lists:
        # Create an event
        event = factory.event.create_or_read(
            name="test",
            tags=["remove_me"],
            threat_actors=["remove_me"],
            threats=["remove_me"],
            db=db,
            history_username="analyst",
        )
        initial_event_version = event.version

        for value in value_list:
            helper_create_func(value=value, db=db)

        # Update the event
        update = client.patch(
            "/api/event/", json=[{key: value_list, "uuid": str(event.uuid), "history_username": "analyst"}]
        )
        assert update.status_code == status.HTTP_204_NO_CONTENT
        assert len(getattr(event, key)) == len(set(value_list))
        assert event.version != initial_event_version

        # Verify the history
        if value_list:
            history = client.get(f"/api/event/{event.uuid}/history")
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
        ("alert_time", "2021-01-01T00:00:00+00:00", None),
        ("alert_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("alert_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("alert_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("alert_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("alert_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("contain_time", "2021-01-01T00:00:00+00:00", None),
        ("contain_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("contain_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("contain_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("contain_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("contain_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("disposition_time", "2021-01-01T00:00:00+00:00", None),
        ("disposition_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("disposition_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("disposition_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("disposition_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("disposition_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("event_time", "2021-01-01T00:00:00+00:00", None),
        ("event_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("ownership_time", "2021-01-01T00:00:00+00:00", None),
        ("ownership_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("ownership_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("ownership_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("ownership_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("ownership_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("remediation_time", "2021-01-01T00:00:00+00:00", None),
        ("remediation_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("remediation_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("remediation_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("remediation_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("remediation_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("name", "test", "test2"),
        ("name", "test", "test"),
    ],
)
def test_update(client, db, key, initial_value, updated_value):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Set the initial value
    setattr(event, key, initial_value)

    # Update it
    update = client.patch(
        "/api/event/", json=[{key: updated_value, "uuid": str(event.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Verify the history
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == key
    assert history.json()["items"][1]["diff"]["old_value"] == initial_value

    # If the test is for one of the times, make sure that the retrieved value matches the proper UTC timestamp
    if key.endswith("_time") and updated_value:
        assert getattr(event, key) == parse("2022-01-01T00:00:00+00:00")
        assert history.json()["items"][1]["diff"]["new_value"] == parse("2022-01-01T00:00:00+00:00").isoformat()
    else:
        assert getattr(event, key) == updated_value
        assert history.json()["items"][1]["diff"]["new_value"] == updated_value
    assert history.json()["items"][1]["snapshot"]["name"] == event.name

    assert event.version != initial_event_version
