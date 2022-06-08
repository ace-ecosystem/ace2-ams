import pytest

from datetime import timedelta
from uuid import uuid4

from api_models.submission import SubmissionUpdate
from db import crud
from exceptions.db import VersionMismatch
from tests.db_tests.crud.node import VALID_LIST_STRING_VALUES
from tests import factory


#
# INVALID TESTS
#


def test_update_version_mismatch(db):
    submission = factory.submission.create(db=db)

    with pytest.raises(VersionMismatch):
        crud.submission.update(model=SubmissionUpdate(uuid=submission.uuid, tags=["tag"], version=uuid4()), db=db)


#
# VALID TESTS
#


def test_update_disposition(db):
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_version = submission.version

    # Create a user
    factory.user.create_or_read(username="analyst", db=db)

    # Create a disposition
    factory.alert_disposition.create_or_read(value="test", rank=1, db=db)

    # Update the disposition
    crud.submission.update(
        model=SubmissionUpdate(uuid=submission.uuid, disposition="test", history_username="analyst"), db=db
    )
    assert submission.disposition.value == "test"
    assert submission.version != initial_version

    # Verify the history
    assert len(submission.history) == 2
    assert submission.history[1].action == "UPDATE"
    assert submission.history[1].action_by.username == "analyst"
    assert submission.history[1].field == "disposition"
    assert submission.history[1].diff["old_value"] is None
    assert submission.history[1].diff["new_value"] == "test"
    assert submission.history[1].snapshot["disposition"]["value"] == "test"

    # Set it back to None
    crud.submission.update(
        model=SubmissionUpdate(uuid=submission.uuid, disposition=None, history_username="analyst"), db=db
    )
    assert submission.disposition is None

    # Verify the history
    assert len(submission.history) == 3
    assert submission.history[2].action == "UPDATE"
    assert submission.history[2].action_by.username == "analyst"
    assert submission.history[2].field == "disposition"
    assert submission.history[2].diff["old_value"] == "test"
    assert submission.history[2].diff["new_value"] is None
    assert submission.history[2].snapshot["disposition"] is None


def test_update_event_uuid(db):
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Update the submission to add it to the event
    crud.submission.update(
        model=SubmissionUpdate(uuid=submission.uuid, event_uuid=event.uuid, history_username="analyst"), db=db
    )
    assert submission.event_uuid == event.uuid
    assert submission.version != initial_submission_version

    # Verify the history
    assert len(submission.history) == 2
    assert submission.history[1].action == "UPDATE"
    assert submission.history[1].action_by.username == "analyst"
    assert submission.history[1].field == "event_uuid"
    assert submission.history[1].diff["old_value"] is None
    assert submission.history[1].diff["new_value"] == str(event.uuid)
    assert submission.history[1].snapshot["event_uuid"] == str(event.uuid)

    # By adding the submission to the event, you should be able to see the submission UUID in the event's
    # alert_uuids list even though it was not explicitly added.
    db.commit()
    assert event.alert_uuids == [submission.uuid]

    # Additionally, adding the submission to the event should trigger the event to have a new version.
    assert event.version != initial_event_version

    # Set it back to None
    crud.submission.update(
        model=SubmissionUpdate(uuid=submission.uuid, event_uuid=None, history_username="analyst"), db=db
    )
    assert submission.event is None

    # Verify the history
    assert len(submission.history) == 3
    assert submission.history[2].action == "UPDATE"
    assert submission.history[2].action_by.username == "analyst"
    assert submission.history[2].field == "event_uuid"
    assert submission.history[2].diff["old_value"] == str(event.uuid)
    assert submission.history[2].diff["new_value"] is None
    assert submission.history[2].snapshot["event_uuid"] is None


def test_update_owner(db):
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Create a user
    factory.user.create_or_read(username="johndoe", db=db)

    # Update the owner
    crud.submission.update(
        model=SubmissionUpdate(uuid=submission.uuid, owner="johndoe", history_username="analyst"), db=db
    )
    assert submission.owner.username == "johndoe"
    assert submission.version != initial_submission_version

    # Verify the history
    assert len(submission.history) == 2
    assert submission.history[1].action == "UPDATE"
    assert submission.history[1].action_by.username == "analyst"
    assert submission.history[1].field == "owner"
    assert submission.history[1].diff["old_value"] is None
    assert submission.history[1].diff["new_value"] == "johndoe"
    assert submission.history[1].snapshot["owner"]["username"] == "johndoe"

    # Set it back to None
    crud.submission.update(model=SubmissionUpdate(uuid=submission.uuid, owner=None, history_username="analyst"), db=db)
    assert submission.owner is None

    # Verify the history
    assert len(submission.history) == 3
    assert submission.history[2].action == "UPDATE"
    assert submission.history[2].action_by.username == "analyst"
    assert submission.history[2].field == "owner"
    assert submission.history[2].diff["old_value"] == "johndoe"
    assert submission.history[2].diff["new_value"] is None
    assert submission.history[2].snapshot["owner"] is None


def test_update_queue(db):
    submission = factory.submission.create(alert_queue="external", db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Create a new submission queue
    factory.queue.create_or_read(value="updated_queue", db=db)

    # Update the queue
    crud.submission.update(
        model=SubmissionUpdate(uuid=submission.uuid, queue="updated_queue", history_username="analyst"), db=db
    )
    assert submission.queue.value == "updated_queue"
    assert submission.version != initial_submission_version

    # Verify the history
    assert len(submission.history) == 2
    assert submission.history[1].action == "UPDATE"
    assert submission.history[1].action_by.username == "analyst"
    assert submission.history[1].field == "queue"
    assert submission.history[1].diff["old_value"] == "external"
    assert submission.history[1].diff["new_value"] == "updated_queue"
    assert submission.history[1].snapshot["queue"]["value"] == "updated_queue"


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
        submission = factory.submission.create(
            tags=["remove_me"],
            threat_actors=["remove_me"],
            threats=["remove_me"],
            db=db,
            history_username="analyst",
        )
        initial_submission_version = submission.version

        for value in value_list:
            helper_create_func(value=value, db=db)

        # Update the submission
        update_model = SubmissionUpdate(uuid=submission.uuid, history_username="analyst")
        setattr(update_model, key, value_list)
        crud.submission.update(model=update_model, db=db)
        assert len(getattr(submission, key)) == len(set(value_list))
        assert submission.version != initial_submission_version

        # Verify the history
        if value_list:
            assert len(submission.history) == 2
            assert submission.history[1].action == "UPDATE"
            assert submission.history[1].action_by.username == "analyst"
            assert submission.history[1].field == key
            assert submission.history[1].diff["old_value"] is None
            assert submission.history[1].diff["new_value"] is None
            assert submission.history[1].diff["added_to_list"] == sorted(set(value_list))
            assert submission.history[1].diff["removed_from_list"] == ["remove_me"]
            assert len(submission.history[1].snapshot[key]) == len(set(value_list))


NOW = crud.helpers.utcnow()
UPDATED_TIME = NOW + timedelta(days=1)


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", None),
        ("event_time", NOW, UPDATED_TIME),
        ("instructions", None, "test"),
        ("instructions", "test", None),
    ],
)
def test_update(db, key, initial_value, updated_value):
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Set the initial value on the submission
    setattr(submission, key, initial_value)
    assert getattr(submission, key) == initial_value

    # Update it
    update_model = SubmissionUpdate(uuid=submission.uuid, history_username="analyst")
    setattr(update_model, key, updated_value)
    crud.submission.update(model=update_model, db=db)
    assert submission.version != initial_submission_version

    # Verify the history
    assert len(submission.history) == 2
    assert submission.history[1].action == "UPDATE"
    assert submission.history[1].action_by.username == "analyst"
    assert submission.history[1].field == key
    assert submission.history[1].snapshot["name"] == "Test Alert"

    old_value = initial_value
    if key.endswith("_time"):
        old_value = initial_value.isoformat()

    new_value = updated_value
    if key.endswith("_time") and updated_value:
        new_value = updated_value.isoformat()

    assert submission.history[1].diff["old_value"] == old_value
    assert submission.history[1].diff["new_value"] == new_value
