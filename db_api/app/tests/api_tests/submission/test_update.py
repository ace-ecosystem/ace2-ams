import pytest
import uuid

from dateutil.parser import parse
from fastapi import status

from tests.api_tests.helpers import INVALID_LIST_STRING_VALUES, VALID_LIST_STRING_VALUES
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
    update = client.patch("/api/submission/", json=[{key: value, "uuid": str(uuid.uuid4())}])
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,values",
    [
        ("tags", INVALID_LIST_STRING_VALUES),
    ],
)
def test_update_invalid_list_fields(client, key, values):
    for value in values:
        update = client.patch("/api/submission/", json=[{key: value, "uuid": str(uuid.uuid4())}])
        assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in update.json()["detail"][0]["loc"]


def test_update_invalid_uuid(client):
    update = client.patch("/api/submission/", json=[{"uuid": "1"}])
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client, db):
    submission = factory.submission.create(db=db)

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client.patch("/api/submission/", json=[{"version": str(uuid.uuid4()), "uuid": str(submission.uuid)}])
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
    submission = factory.submission.create(db=db)

    # Make sure you cannot update it to use a nonexistent field value
    update = client.patch(
        "/api/submission/", json=[{key: value, "uuid": str(submission.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key",
    [("tags")],
)
def test_update_nonexistent_list_fields(client, db, key):
    submission = factory.submission.create(db=db)

    # Make sure you cannot update it to use a nonexistent list field value
    update = client.patch("/api/submission/", json=[{key: ["abc"], "uuid": str(submission.uuid)}])
    assert update.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in update.text


def test_update_nonexistent_uuid(client):
    update = client.patch("/api/submission/", json=[{"uuid": str(uuid.uuid4())}])
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_disposition(client, db):
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_version = submission.version

    # Create a user
    factory.user.create_or_read(username="analyst", db=db)

    # Create a disposition
    factory.alert_disposition.create_or_read(value="test", rank=1, db=db)

    # Update the disposition
    update = client.patch(
        "/api/submission/", json=[{"disposition": "test", "uuid": str(submission.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.disposition.value == "test"
    assert submission.version != initial_version

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "disposition"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "test"
    assert history.json()["items"][1]["snapshot"]["disposition"]["value"] == "test"

    # Set it back to None
    update = client.patch(
        "/api/submission/", json=[{"disposition": None, "uuid": str(submission.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.disposition is None

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "disposition"
    assert history.json()["items"][2]["diff"]["old_value"] == "test"
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["disposition"] is None


def test_update_event_uuid(client, db):
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Create an event
    event = factory.event.create_or_read(name="test", db=db, history_username="analyst")
    initial_event_version = event.version

    # Update the submission to add it to the event
    update = client.patch(
        "/api/submission/",
        json=[{"event_uuid": str(event.uuid), "uuid": str(submission.uuid), "history_username": "analyst"}],
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.event_uuid == event.uuid
    assert submission.version != initial_submission_version

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "event_uuid"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == str(event.uuid)
    assert history.json()["items"][1]["snapshot"]["event_uuid"] == str(event.uuid)

    # By adding the submission to the event, you should be able to see the submission UUID in the event's
    # alert_uuids list even though it was not explicitly added.
    assert event.alert_uuids == [submission.uuid]

    # Additionally, adding the submission to the event should trigger the event to have a new version.
    assert event.version != initial_event_version

    # Set it back to None
    update = client.patch(
        "/api/submission/", json=[{"event_uuid": None, "uuid": str(submission.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.event is None

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "event_uuid"
    assert history.json()["items"][2]["diff"]["old_value"] == str(event.uuid)
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["event_uuid"] is None


def test_update_owner(client, db):
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Create a user
    factory.user.create_or_read(username="johndoe", db=db)

    # Update the owner
    update = client.patch(
        "/api/submission/", json=[{"owner": "johndoe", "uuid": str(submission.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.owner.username == "johndoe"
    assert submission.version != initial_submission_version

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "owner"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "johndoe"
    assert history.json()["items"][1]["snapshot"]["owner"]["username"] == "johndoe"

    # Set it back to None
    update = client.patch(
        "/api/submission/", json=[{"owner": None, "uuid": str(submission.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.owner is None

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "owner"
    assert history.json()["items"][2]["diff"]["old_value"] == "johndoe"
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["owner"] is None


def test_update_queue(client, db):
    submission = factory.submission.create(alert_queue="external", db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Create a new submission queue
    factory.queue.create_or_read(value="updated_queue", db=db)

    # Update the queue
    update = client.patch(
        "/api/submission/",
        json=[{"queue": "updated_queue", "uuid": str(submission.uuid), "history_username": "analyst"}],
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.queue.value == "updated_queue"
    assert submission.version != initial_submission_version

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
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
        ("tags", VALID_LIST_STRING_VALUES, factory.metadata_tag.create_or_read),
    ],
)
def test_update_valid_list_fields(client, db, key, value_lists, helper_create_func):
    for value_list in value_lists:
        submission = factory.submission.create(
            tags=["remove_me"],
            db=db,
            history_username="analyst",
        )
        initial_submission_version = submission.version

        for value in value_list:
            helper_create_func(value=value, db=db)

        # Update the submission
        update = client.patch(
            "/api/submission/", json=[{key: value_list, "uuid": str(submission.uuid), "history_username": "analyst"}]
        )
        assert update.status_code == status.HTTP_204_NO_CONTENT
        assert len(getattr(submission, key)) == len(set(value_list))
        assert submission.version != initial_submission_version

        # Verify the history
        if value_list:
            history = client.get(f"/api/submission/{submission.uuid}/history")
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
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Set the initial value on the submission
    setattr(submission, key, initial_value)
    assert getattr(submission, key) == initial_value

    # Update it
    update = client.patch(
        "/api/submission/", json=[{key: updated_value, "uuid": str(submission.uuid), "history_username": "analyst"}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == key
    assert history.json()["items"][1]["diff"]["old_value"] == initial_value

    if key == "event_time":
        assert submission.event_time == parse("2022-01-01T00:00:00+00:00")
        assert history.json()["items"][1]["diff"]["new_value"] == parse("2022-01-01T00:00:00+00:00").isoformat()
    else:
        assert getattr(submission, key) == updated_value
        assert history.json()["items"][1]["diff"]["new_value"] == updated_value
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"

    assert submission.version != initial_submission_version


def test_update_multiple_submissions(client, db):
    submission1 = factory.submission.create(db=db, history_username="analyst")
    initial_submission1_version = submission1.version

    submission2 = factory.submission.create(db=db, history_username="analyst")
    initial_submission2_version = submission2.version
    initial_event_time = submission2.event_time.isoformat()

    submission3 = factory.submission.create(db=db, history_username="analyst")
    initial_submission3_version = submission3.version

    assert submission1.description is None
    assert submission2.event_time != parse("2022-01-01T00:00:00+00:00")
    assert submission3.instructions is None

    # Update all the submissions at once
    update_data = [
        {"description": "updated_description", "uuid": str(submission1.uuid), "history_username": "analyst"},
        {"event_time": "2022-01-01 00:00:00+00:00", "uuid": str(submission2.uuid), "history_username": "analyst"},
        {"instructions": "updated_instructions", "uuid": str(submission3.uuid), "history_username": "analyst"},
    ]
    update = client.patch("/api/submission/", json=update_data)
    assert update.status_code == status.HTTP_204_NO_CONTENT

    assert submission1.description == "updated_description"
    assert submission1.version != initial_submission1_version

    assert submission2.event_time == parse("2022-01-01T00:00:00+00:00")
    assert submission2.version != initial_submission2_version

    assert submission3.instructions == "updated_instructions"
    assert submission3.version != initial_submission3_version

    # Verify the history
    history = client.get(f"/api/submission/{submission1.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "description"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "updated_description"
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"

    history = client.get(f"/api/submission/{submission2.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "event_time"
    assert history.json()["items"][1]["diff"]["old_value"] == initial_event_time
    assert history.json()["items"][1]["diff"]["new_value"] == parse("2022-01-01T00:00:00+00:00").isoformat()
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"

    history = client.get(f"/api/submission/{submission3.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "instructions"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == "updated_instructions"
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"


def test_update_multiple_fields(client, db):
    submission = factory.submission.create(db=db, history_username="analyst")
    initial_submission_version = submission.version

    # Update it
    update = client.patch(
        "/api/submission/",
        json=[
            {
                "description": "updated_description",
                "history_username": "analyst",
                "instructions": "updated_instructions",
                "uuid": str(submission.uuid),
            }
        ],
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.version != initial_submission_version

    # Verify the history
    history = client.get(f"/api/submission/{submission.uuid}/history")
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
