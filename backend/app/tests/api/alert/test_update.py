import pytest
import uuid

from dateutil.parser import parse
from fastapi import status

from tests.api.node import (
    INVALID_UPDATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTORS,
    VALID_THREATS,
)
from tests import helpers


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
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/alert/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_UPDATE_FIELDS,
)
def test_update_invalid_node_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/alert/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/alert/1", json={})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key,value",
    [
        ("disposition", "abc"),
        ("event_uuid", str(uuid.uuid4())),
        ("owner", "johndoe"),
        ("queue", "abc"),
    ],
)
def test_update_nonexistent_fields(client_valid_access_token, db, key, value):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Make sure you cannot update it to use a nonexistent field value
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={key: value})
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_update_nonexistent_node_fields(client_valid_access_token, db, key, value):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={key: value})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/alert/{uuid.uuid4()}", json={})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_disposition(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_version = alert.version

    # Create a user
    helpers.create_user(username="analyst", db=db)

    # Create a disposition
    helpers.create_alert_disposition(value="test", rank=1, db=db)

    # Update the disposition
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"disposition": "test"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.disposition.value == "test"
    assert alert.version != initial_version


def test_update_event_uuid(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Update the alert to add it to the event
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"event_uuid": str(event.uuid)})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.event_uuid == event.uuid
    assert alert.version != initial_alert_version

    # By adding the alert to the event, you should be able to see the alert UUID in the event's
    # alert_uuids list even though it was not explicitly added.
    assert event.alert_uuids == [alert.uuid]

    # Additionally, adding the alert to the event should trigger the event to have a new version.
    assert event.version != initial_event_version


def test_update_owner(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Create a user
    helpers.create_user(username="johndoe", db=db)

    # Update the owner
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"owner": "johndoe"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.owner.username == "johndoe"
    assert alert.version != initial_alert_version


def test_update_queue(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Create a new alert queue
    helpers.create_alert_queue(value="test_queue2", db=db)

    # Update the queue
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"queue": "test_queue2"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert.queue.value == "test_queue2"
    assert alert.version != initial_alert_version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_update_valid_node_directives(client_valid_access_token, db, values):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Create the directives
    for value in values:
        helpers.create_node_directive(value=value, db=db)

    # Update the alert
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"directives": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(alert.directives) == len(set(values))
    assert alert.version != initial_alert_version


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_update_valid_node_tags(client_valid_access_token, db, values):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Create the tags
    for value in values:
        helpers.create_node_tag(value=value, db=db)

    # Update the alert
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"tags": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(alert.tags) == len(set(values))
    assert alert.version != initial_alert_version


@pytest.mark.parametrize(
    "values",
    VALID_THREAT_ACTORS,
)
def test_update_valid_node_threat_actors(client_valid_access_token, db, values):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Create the threat actor
    for value in values:
        helpers.create_node_threat_actor(value=value, db=db)

    # Update the alert
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"threat_actors": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(alert.threat_actors) == len(set(values))
    assert alert.version != initial_alert_version


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_update_valid_node_threats(client_valid_access_token, db, values):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Create the threats
    for value in values:
        helpers.create_node_threat(value=value, types=["test_type"], db=db)

    # Update the alert
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={"threats": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(alert.threats) == len(set(values))
    assert alert.version != initial_alert_version


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", None),
        ("description", "test", "test"),
        ("event_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("instructions", None, "test"),
        ("instructions", "test", None),
        ("instructions", "test", "test"),
    ],
)
def test_update(client_valid_access_token, db, key, initial_value, updated_value):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Set the initial value on the alert
    setattr(alert, key, initial_value)
    assert getattr(alert, key) == initial_value

    # Update it
    update = client_valid_access_token.patch(f"/api/alert/{alert.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if key == "event_time":
        assert alert.event_time == parse("2022-01-01T00:00:00+00:00")
    else:
        assert getattr(alert, key) == updated_value

    assert alert.version != initial_alert_version
