import pytest
import uuid

from dateutil.parser import parse
from fastapi import status

from tests.api.node import (
    INVALID_UPDATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTOR,
    VALID_THREATS,
)
from tests import helpers


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
        ("remediation_time", ""),
        ("remediation_time", "Monday"),
        ("remediation_time", "2022-01-01"),
        ("remediations", None),
        ("remediations", "test_type"),
        ("remediations", [123]),
        ("remediations", [None]),
        ("remediations", [""]),
        ("remediations", ["abc", 123]),
        ("risk_level", 123),
        ("risk_level", ""),
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
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/event/{uuid.uuid4()}", json={key: value, "version": str(uuid.uuid4())}
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_UPDATE_FIELDS,
)
def test_update_invalid_node_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/event/{uuid.uuid4()}", json={"version": str(uuid.uuid4()), key: value}
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/event/1", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token, db):
    # create an event
    event = helpers.create_event(name="test", db=db)

    # Make sure you cannot update it using an invalid version
    update = client_valid_access_token.patch(f"/api/event/{event.uuid}", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key,value",
    [
        ("owner", "johndoe"),
        ("prevention_tools", ["abc"]),
        ("remediations", ["abc"]),
        ("risk_level", "abc"),
        ("source", "abc"),
        ("status", "abc"),
        ("type", "abc"),
        ("vectors", ["abc"]),
    ],
)
def test_update_nonexistent_fields(client_valid_access_token, db, key, value):
    # Create an event
    event = helpers.create_event(name="test", db=db)

    # Make sure you cannot update it to use a nonexistent field value
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={key: value, "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_update_nonexistent_node_fields(client_valid_access_token, db, key, value):
    # Create an event
    event = helpers.create_event(name="test", db=db)

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={key: value, "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/event/{uuid.uuid4()}", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_owner(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create a user
    helpers.create_user(username="johndoe", db=db)

    # Update the event
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"owner": "johndoe", "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.owner.username == "johndoe"
    assert event.version != initial_event_version


def test_update_prevention_tools(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create an event prevention tool
    helpers.create_event_prevention_tool(value="test", db=db)

    # Update the event
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"prevention_tools": ["test"], "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(event.prevention_tools) == 1
    assert event.prevention_tools[0].value == "test"
    assert event.version != initial_event_version


def test_update_remediations(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create an event remediation
    helpers.create_event_remediation(value="test", db=db)

    # Update the event
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"remediations": ["test"], "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(event.remediations) == 1
    assert event.remediations[0].value == "test"
    assert event.version != initial_event_version


def test_update_risk_level(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create an event risk level
    helpers.create_event_risk_level(value="test", db=db)

    # Update the event
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"risk_level": "test", "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.risk_level.value == "test"
    assert event.version != initial_event_version


def test_update_source(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create an event source
    helpers.create_event_source(value="test", db=db)

    # Update the event
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"source": "test", "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.source.value == "test"
    assert event.version != initial_event_version


def test_update_status(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create an event status
    helpers.create_event_status(value="test", db=db)

    # Update the event
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"status": "test", "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.status.value == "test"
    assert event.version != initial_event_version


def test_update_type(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create an event type
    helpers.create_event_type(value="test", db=db)

    # Update the event
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"type": "test", "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert event.type.value == "test"
    assert event.version != initial_event_version


def test_update_vectors(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create an event vector
    helpers.create_event_vector(value="test", db=db)

    # Update the event
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"vectors": ["test"], "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(event.vectors) == 1
    assert event.vectors[0].value == "test"
    assert event.version != initial_event_version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_update_valid_node_directives(client_valid_access_token, db, values):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create the directives
    for value in values:
        helpers.create_node_directive(value=value, db=db)

    # Update the node
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"directives": values, "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(event.directives) == len(set(values))
    assert event.version != initial_event_version


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_update_valid_node_tags(client_valid_access_token, db, values):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create the tags
    for value in values:
        helpers.create_node_tag(value=value, db=db)

    # Update the node
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"tags": values, "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(event.tags) == len(set(values))
    assert event.version != initial_event_version


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_update_valid_node_threat_actor(client_valid_access_token, db, value):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create the threat actor
    if value:
        helpers.create_node_threat_actor(value=value, db=db)

    # Update the node
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"threat_actor": value, "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if value:
        assert event.threat_actor.value == value
    else:
        assert event.threat_actor is None

    assert event.version != initial_event_version


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_update_valid_node_threats(client_valid_access_token, db, values):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Create the threats
    for value in values:
        helpers.create_node_threat(value=value, types=["test_type"], db=db)

    # Update the node
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"threats": values, "version": str(event.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    assert len(event.threats) == len(set(values))
    assert event.version != initial_event_version


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
def test_update(client_valid_access_token, db, key, initial_value, updated_value):
    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Set the initial value
    setattr(event, key, initial_value)

    # Update it
    update = client_valid_access_token.patch(
        f"/api/event/{event.uuid}", json={"version": str(event.version), key: updated_value}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # If the test is for one of the times, make sure that the retrieved value matches the proper UTC timestamp
    if key.endswith("_time") and updated_value:
        assert getattr(event, key) == parse("2022-01-01T00:00:00+00:00")
    else:
        assert getattr(event, key) == updated_value

    assert event.version != initial_event_version
