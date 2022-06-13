import pytest

from datetime import timedelta
from uuid import uuid4

from api_models.event import EventUpdate
from db import crud
from exceptions.db import VersionMismatch
from tests.db_tests.crud.node import VALID_LIST_STRING_VALUES
from tests import factory


#
# INVALID TESTS
#


def test_update_version_mismatch(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")

    # Update the event
    with pytest.raises(VersionMismatch):
        crud.event.update(uuid=event.uuid, model=EventUpdate(name="test2", version=uuid4()), db=db)


#
# VALID TESTS
#


def test_update_owner(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create a user
    factory.user.create_or_read(username="johndoe", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(owner="johndoe", history_username="analyst"), db=db)
    assert event.owner.username == "johndoe"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "owner"
    assert event.history[1].diff["old_value"] is None
    assert event.history[1].diff["new_value"] == "johndoe"
    assert event.history[1].snapshot["owner"]["username"] == "johndoe"

    # Set it back to None
    crud.event.update(uuid=event.uuid, model=EventUpdate(owner=None, history_username="analyst"), db=db)
    assert event.owner is None

    # Verify the history
    assert len(event.history) == 3
    assert event.history[2].action == "UPDATE"
    assert event.history[2].action_by.username == "analyst"
    assert event.history[2].field == "owner"
    assert event.history[2].diff["old_value"] == "johndoe"
    assert event.history[2].diff["new_value"] is None
    assert event.history[2].snapshot["owner"] is None


def test_update_prevention_tools(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event prevention tool
    factory.event_prevention_tool.create_or_read(value="test", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(prevention_tools=["test"], history_username="analyst"), db=db)
    assert len(event.prevention_tools) == 1
    assert event.prevention_tools[0].value == "test"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "prevention_tools"
    assert event.history[1].diff["old_value"] is None
    assert event.history[1].diff["new_value"] is None
    assert event.history[1].diff["added_to_list"] == ["test"]
    assert event.history[1].diff["removed_from_list"] == []
    assert event.history[1].snapshot["prevention_tools"][0]["value"] == "test"

    # Set it back to an empty list
    crud.event.update(uuid=event.uuid, model=EventUpdate(prevention_tools=[], history_username="analyst"), db=db)
    assert event.prevention_tools == []

    # Verify the history
    assert len(event.history) == 3
    assert event.history[2].action == "UPDATE"
    assert event.history[2].action_by.username == "analyst"
    assert event.history[2].field == "prevention_tools"
    assert event.history[2].diff["old_value"] is None
    assert event.history[2].diff["new_value"] is None
    assert event.history[2].diff["added_to_list"] == []
    assert event.history[2].diff["removed_from_list"] == ["test"]
    assert event.history[2].snapshot["prevention_tools"] == []


def test_update_queue(db):
    # Create an event
    event = factory.event.create_or_read(name="test", event_queue="external", db=db, history_username="analyst")
    initial_event_version = event.version
    assert event.queue.value == "external"

    # Create an event queue
    factory.queue.create_or_read(value="updated_queue", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(queue="updated_queue", history_username="analyst"), db=db)
    assert event.queue.value == "updated_queue"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "queue"
    assert event.history[1].diff["old_value"] == "external"
    assert event.history[1].diff["new_value"] == "updated_queue"
    assert event.history[1].snapshot["queue"]["value"] == "updated_queue"


def test_update_remediations(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event remediation
    factory.event_remediation.create_or_read(value="test", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(remediations=["test"], history_username="analyst"), db=db)
    assert len(event.remediations) == 1
    assert event.remediations[0].value == "test"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "remediations"
    assert event.history[1].diff["old_value"] is None
    assert event.history[1].diff["new_value"] is None
    assert event.history[1].diff["added_to_list"] == ["test"]
    assert event.history[1].diff["removed_from_list"] == []
    assert event.history[1].snapshot["remediations"][0]["value"] == "test"

    # Set it back to an empty list
    crud.event.update(uuid=event.uuid, model=EventUpdate(remediations=[], history_username="analyst"), db=db)
    assert event.remediations == []

    # Verify the history
    assert len(event.history) == 3
    assert event.history[2].action == "UPDATE"
    assert event.history[2].action_by.username == "analyst"
    assert event.history[2].field == "remediations"
    assert event.history[2].diff["old_value"] is None
    assert event.history[2].diff["new_value"] is None
    assert event.history[2].diff["added_to_list"] == []
    assert event.history[2].diff["removed_from_list"] == ["test"]
    assert event.history[2].snapshot["remediations"] == []


def test_update_severity(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event severity
    factory.event_severity.create_or_read(value="test", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(severity="test", history_username="analyst"), db=db)
    assert event.severity.value == "test"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "severity"
    assert event.history[1].diff["old_value"] is None
    assert event.history[1].diff["new_value"] == "test"
    assert event.history[1].snapshot["severity"]["value"] == "test"

    # Set it back to None
    crud.event.update(uuid=event.uuid, model=EventUpdate(severity=None, history_username="analyst"), db=db)
    assert event.severity is None

    # Verify the history
    assert len(event.history) == 3
    assert event.history[2].action == "UPDATE"
    assert event.history[2].action_by.username == "analyst"
    assert event.history[2].field == "severity"
    assert event.history[2].diff["old_value"] == "test"
    assert event.history[2].diff["new_value"] is None
    assert event.history[2].snapshot["severity"] is None


def test_update_source(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event source
    factory.event_source.create_or_read(value="test", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(source="test", history_username="analyst"), db=db)
    assert event.source.value == "test"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "source"
    assert event.history[1].diff["old_value"] is None
    assert event.history[1].diff["new_value"] == "test"
    assert event.history[1].snapshot["source"]["value"] == "test"

    # Set it back to None
    crud.event.update(uuid=event.uuid, model=EventUpdate(source=None, history_username="analyst"), db=db)
    assert event.source is None

    # Verify the history
    assert len(event.history) == 3
    assert event.history[2].action == "UPDATE"
    assert event.history[2].action_by.username == "analyst"
    assert event.history[2].field == "source"
    assert event.history[2].diff["old_value"] == "test"
    assert event.history[2].diff["new_value"] is None
    assert event.history[2].snapshot["source"] is None


def test_update_status(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event status
    factory.event_status.create_or_read(value="test", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(status="test", history_username="analyst"), db=db)
    assert event.status.value == "test"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "status"
    assert event.history[1].diff["old_value"] == "OPEN"
    assert event.history[1].diff["new_value"] == "test"
    assert event.history[1].snapshot["status"]["value"] == "test"


def test_update_type(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event type
    factory.event_type.create_or_read(value="test", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(type="test", history_username="analyst"), db=db)
    assert event.type.value == "test"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "type"
    assert event.history[1].diff["old_value"] is None
    assert event.history[1].diff["new_value"] == "test"
    assert event.history[1].snapshot["type"]["value"] == "test"

    # Set it back to None
    crud.event.update(uuid=event.uuid, model=EventUpdate(type=None, history_username="analyst"), db=db)
    assert event.type is None

    # Verify the history
    assert len(event.history) == 3
    assert event.history[2].action == "UPDATE"
    assert event.history[2].action_by.username == "analyst"
    assert event.history[2].field == "type"
    assert event.history[2].diff["old_value"] == "test"
    assert event.history[2].diff["new_value"] is None
    assert event.history[2].snapshot["type"] is None


def test_update_vectors(db):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Create an event vector
    factory.event_vector.create_or_read(value="test", db=db)

    # Update the event
    crud.event.update(uuid=event.uuid, model=EventUpdate(vectors=["test"], history_username="analyst"), db=db)
    assert len(event.vectors) == 1
    assert event.vectors[0].value == "test"
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == "vectors"
    assert event.history[1].diff["old_value"] is None
    assert event.history[1].diff["new_value"] is None
    assert event.history[1].diff["added_to_list"] == ["test"]
    assert event.history[1].diff["removed_from_list"] == []
    assert event.history[1].snapshot["vectors"][0]["value"] == "test"

    # Set it back to an empty list
    crud.event.update(uuid=event.uuid, model=EventUpdate(vectors=[], history_username="analyst"), db=db)
    assert event.vectors == []

    # Verify the history
    assert len(event.history) == 3
    assert event.history[2].action == "UPDATE"
    assert event.history[2].action_by.username == "analyst"
    assert event.history[2].field == "vectors"
    assert event.history[2].diff["old_value"] is None
    assert event.history[2].diff["new_value"] is None
    assert event.history[2].diff["added_to_list"] == []
    assert event.history[2].diff["removed_from_list"] == ["test"]
    assert event.history[2].snapshot["vectors"] == []


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("tags", VALID_LIST_STRING_VALUES, factory.node_tag.create_or_read),
        ("threat_actors", VALID_LIST_STRING_VALUES, factory.node_threat_actor.create_or_read),
        ("threats", VALID_LIST_STRING_VALUES, factory.node_threat.create_or_read),
    ],
)
def test_update_valid_node_fields(db, key, value_lists, helper_create_func):
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
        update_model = EventUpdate(history_username="analyst")
        setattr(update_model, key, value_list)
        crud.event.update(uuid=event.uuid, model=update_model, db=db)
        assert len(getattr(event, key)) == len(set(value_list))
        assert event.version != initial_event_version

        # Verify the history
        if value_list:
            assert len(event.history) == 2
            assert event.history[1].action == "UPDATE"
            assert event.history[1].action_by.username == "analyst"
            assert event.history[1].field == key
            assert event.history[1].diff["old_value"] is None
            assert event.history[1].diff["new_value"] is None
            assert event.history[1].diff["added_to_list"] == sorted(set(value_list))
            assert event.history[1].diff["removed_from_list"] == ["remove_me"]
            assert len(event.history[1].snapshot[key]) == len(set(value_list))


NOW = crud.helpers.utcnow()
UPDATED_TIME = NOW + timedelta(days=1)


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("alert_time", NOW, None),
        ("alert_time", NOW, UPDATED_TIME),
        ("contain_time", NOW, None),
        ("contain_time", NOW, UPDATED_TIME),
        ("disposition_time", NOW, None),
        ("disposition_time", NOW, UPDATED_TIME),
        ("event_time", NOW, None),
        ("event_time", NOW, UPDATED_TIME),
        ("ownership_time", NOW, None),
        ("ownership_time", NOW, UPDATED_TIME),
        ("remediation_time", NOW, None),
        ("remediation_time", NOW, UPDATED_TIME),
        ("name", "test", "test2"),
        ("name", "test", "test"),
    ],
)
def test_update(db, key, initial_value, updated_value):
    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Set the initial value
    setattr(event, key, initial_value)

    # Update it
    update_model = EventUpdate(history_username="analyst")
    setattr(update_model, key, updated_value)
    crud.event.update(uuid=event.uuid, model=update_model, db=db)
    assert event.version != initial_event_version

    # Verify the history
    assert len(event.history) == 2
    assert event.history[1].action == "UPDATE"
    assert event.history[1].action_by.username == "analyst"
    assert event.history[1].field == key
    assert event.history[1].snapshot["name"] == event.name

    old_value = initial_value
    if key.endswith("_time"):
        old_value = initial_value.isoformat()

    new_value = updated_value
    if key.endswith("_time") and updated_value:
        new_value = updated_value.isoformat()

    assert event.history[1].diff["old_value"] == old_value
    assert event.history[1].diff["new_value"] == new_value
