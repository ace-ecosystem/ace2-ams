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
        ("context", 123),
        ("context", ""),
        ("redirection_uuid", 123),
        ("redirection_uuid", ""),
        ("redirection_uuid", "abc"),
        ("time", None),
        ("time", ""),
        ("time", "Monday"),
        ("time", "2022-01-01"),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{uuid.uuid4()}",
        json={
            key: value,
            "version": str(uuid.uuid4()),
        },
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_UPDATE_FIELDS,
)
def test_update_invalid_node_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{uuid.uuid4()}",
        json={
            "version": str(uuid.uuid4()),
            key: value,
        },
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/observable/instance/1", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token, db):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )

    # Make sure you cannot update it using an invalid version
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj.uuid}", json={"version": str(uuid.uuid4())}
    )
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_redirection_uuid(client_valid_access_token, db):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )

    # Make sure you cannot update it to use a nonexistent redirection UUID
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj.uuid}",
        json={"redirection_uuid": str(uuid.uuid4()), "version": str(obj.version)},
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_update_nonexistent_node_fields(client_valid_access_token, db, key, value):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj.uuid}", json={key: value, "version": str(obj.version)}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{uuid.uuid4()}", json={"version": str(uuid.uuid4())}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_redirection_uuid(client_valid_access_token, db):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj1 = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )
    initial_observable_instance_version = obj1.version
    assert obj1.redirection is None

    # Create a second observable instance to use for redirection
    obj2 = helpers.create_observable_instance(
        type="test_type", value="test2", alert=alert, parent_analysis=root_analysis, db=db
    )

    # Update the redirection UUID
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj1.uuid}", json={"redirection_uuid": str(obj2.uuid), "version": str(obj1.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert obj1.redirection_uuid == obj2.uuid
    assert obj1.version != initial_observable_instance_version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_update_valid_node_directives(client_valid_access_token, db, values):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )
    initial_observable_instance_version = obj.version
    assert obj.directives == []

    # Create the directives
    for value in values:
        helpers.create_node_directive(value=value, db=db)

    # Update the node
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj.uuid}", json={"directives": values, "version": str(obj.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(obj.directives) == len(set(values))
    assert obj.version != initial_observable_instance_version


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_update_valid_node_tags(client_valid_access_token, db, values):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )
    initial_observable_instance_version = obj.version
    assert obj.tags == []

    # Create the tags
    for value in values:
        helpers.create_node_tag(value=value, db=db)

    # Update the node
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj.uuid}", json={"tags": values, "version": str(obj.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(obj.tags) == len(set(values))
    assert obj.version != initial_observable_instance_version


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_update_valid_node_threat_actor(client_valid_access_token, db, value):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )
    initial_observable_instance_version = obj.version
    assert obj.threat_actor is None

    # Create the threat actor
    if value:
        helpers.create_node_threat_actor(value=value, db=db)

    # Update the node
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj.uuid}", json={"threat_actor": value, "version": str(obj.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if value:
        assert obj.threat_actor.value == value
    else:
        assert obj.threat_actor is None

    assert obj.version != initial_observable_instance_version


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_update_valid_node_threats(client_valid_access_token, db, values):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )
    initial_observable_instance_version = obj.version
    assert obj.threats == []

    # Create the threats
    for value in values:
        helpers.create_node_threat(value=value, types=["test_type"], db=db)

    # Update the node
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj.uuid}", json={"threats": values, "version": str(obj.version)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(obj.threats) == len(set(values))
    assert obj.version != initial_observable_instance_version


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("context", None, "test"),
        ("context", "test", None),
        ("context", "test", "test"),
        ("time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
    ],
)
def test_update(client_valid_access_token, key, db, initial_value, updated_value):
    # Create an alert and analysis
    alert = helpers.create_alert(db=db)
    root_analysis = helpers.create_analysis(db=db, alert=alert)

    # Create an observable instance
    obj = helpers.create_observable_instance(
        type="test_type", value="test", alert=alert, parent_analysis=root_analysis, db=db
    )
    initial_observable_instance_version = obj.version

    # Set the initial value
    setattr(obj, key, initial_value)

    # Update it
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{obj.uuid}", json={"version": str(obj.version), key: updated_value}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if key == "time":
        assert obj.time == parse("2022-01-01T00:00:00+00:00")
    else:
        assert getattr(obj, key) == updated_value

    assert obj.version != initial_observable_instance_version
