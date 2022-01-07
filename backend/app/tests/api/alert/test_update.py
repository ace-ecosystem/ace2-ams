import pytest
import uuid

from dateutil.parser import parse
from fastapi import status

from tests.api.node import INVALID_LIST_STRING_VALUES, VALID_LIST_STRING_VALUES
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
    update = client_valid_access_token.patch("/api/alert/", json=[{key: value, "uuid": str(uuid.uuid4())}])
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
def test_update_invalid_node_fields(client_valid_access_token, key, values):
    for value in values:
        update = client_valid_access_token.patch("/api/alert/", json=[{key: value, "uuid": str(uuid.uuid4())}])
        assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in update.json()["detail"][0]["loc"]


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/alert/", json=[{"uuid": "1"}])
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client_valid_access_token.patch(
        "/api/alert/", json=[{"version": str(uuid.uuid4()), "uuid": str(alert_tree.node_uuid)}]
    )
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
    alert_tree = helpers.create_alert(db=db)

    # Make sure you cannot update it to use a nonexistent field value
    update = client_valid_access_token.patch("/api/alert/", json=[{key: value, "uuid": str(alert_tree.node_uuid)}])
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key",
    [("tags"), ("threat_actors"), ("threats")],
)
def test_update_nonexistent_node_fields(client_valid_access_token, db, key):
    alert_tree = helpers.create_alert(db=db)

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch("/api/alert/", json=[{key: ["abc"], "uuid": str(alert_tree.node_uuid)}])
    assert update.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in update.text


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/alert/", json=[{"uuid": str(uuid.uuid4())}])
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_disposition(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    initial_version = alert_tree.node.version

    # Create a user
    helpers.create_user(username="analyst", db=db)

    # Create a disposition
    helpers.create_alert_disposition(value="test", rank=1, db=db)

    # Update the disposition
    update = client_valid_access_token.patch(
        "/api/alert/", json=[{"disposition": "test", "uuid": str(alert_tree.node_uuid)}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert_tree.node.disposition.value == "test"
    assert alert_tree.node.version != initial_version

    # Set it back to None
    update = client_valid_access_token.patch(
        "/api/alert/", json=[{"disposition": None, "uuid": str(alert_tree.node_uuid)}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert_tree.node.disposition is None


def test_update_event_uuid(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    initial_alert_version = alert_tree.node.version

    # Create an event
    event = helpers.create_event(name="test", db=db)
    initial_event_version = event.version

    # Update the alert to add it to the event
    update = client_valid_access_token.patch(
        "/api/alert/", json=[{"event_uuid": str(event.uuid), "uuid": str(alert_tree.node_uuid)}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert_tree.node.event_uuid == event.uuid
    assert alert_tree.node.version != initial_alert_version

    # By adding the alert to the event, you should be able to see the alert UUID in the event's
    # alert_uuids list even though it was not explicitly added.
    assert event.alert_uuids == [alert_tree.node_uuid]

    # Additionally, adding the alert to the event should trigger the event to have a new version.
    assert event.version != initial_event_version

    # Set it back to None
    update = client_valid_access_token.patch(
        "/api/alert/", json=[{"event_uuid": None, "uuid": str(alert_tree.node_uuid)}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert_tree.node.event is None


def test_update_owner(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    initial_alert_version = alert_tree.node.version

    # Create a user
    helpers.create_user(username="johndoe", db=db)

    # Update the owner
    update = client_valid_access_token.patch(
        "/api/alert/", json=[{"owner": "johndoe", "uuid": str(alert_tree.node_uuid)}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert_tree.node.owner.username == "johndoe"
    assert alert_tree.node.version != initial_alert_version

    # Set it back to None
    update = client_valid_access_token.patch("/api/alert/", json=[{"owner": None, "uuid": str(alert_tree.node_uuid)}])
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert_tree.node.owner is None


def test_update_queue(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    initial_alert_version = alert_tree.node.version

    # Create a new alert queue
    helpers.create_alert_queue(value="test_queue2", db=db)

    # Update the queue
    update = client_valid_access_token.patch(
        "/api/alert/", json=[{"queue": "test_queue2", "uuid": str(alert_tree.node_uuid)}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert alert_tree.node.queue.value == "test_queue2"
    assert alert_tree.node.version != initial_alert_version


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("tags", VALID_LIST_STRING_VALUES, helpers.create_node_tag),
        ("threat_actors", VALID_LIST_STRING_VALUES, helpers.create_node_threat_actor),
        ("threats", VALID_LIST_STRING_VALUES, helpers.create_node_threat),
    ],
)
def test_update_valid_node_fields(client_valid_access_token, db, key, value_lists, helper_create_func):
    for value_list in value_lists:
        alert_tree = helpers.create_alert(db=db)
        initial_alert_version = alert_tree.node.version

        for value in value_list:
            helper_create_func(value=value, db=db)

        helpers.create_alert_queue(value="test_queue", db=db)
        helpers.create_alert_type(value="test_type", db=db)
        helpers.create_observable_type(value="o_type", db=db)

        # Update the alert
        update = client_valid_access_token.patch(
            "/api/alert/", json=[{key: value_list, "uuid": str(alert_tree.node_uuid)}]
        )
        assert update.status_code == status.HTTP_204_NO_CONTENT
        assert len(getattr(alert_tree.node, key)) == len(set(value_list))
        assert alert_tree.node.version != initial_alert_version


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
    alert_tree = helpers.create_alert(db=db)
    initial_alert_version = alert_tree.node.version

    # Set the initial value on the alert
    setattr(alert_tree.node, key, initial_value)
    assert getattr(alert_tree.node, key) == initial_value

    # Update it
    update = client_valid_access_token.patch(
        "/api/alert/", json=[{key: updated_value, "uuid": str(alert_tree.node_uuid)}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if key == "event_time":
        assert alert_tree.node.event_time == parse("2022-01-01T00:00:00+00:00")
    else:
        assert getattr(alert_tree.node, key) == updated_value

    assert alert_tree.node.version != initial_alert_version


def test_update_multiple(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db=db)
    initial_alert1_version = alert_tree1.node.version

    alert_tree2 = helpers.create_alert(db=db)
    initial_alert2_version = alert_tree2.node.version

    alert_tree3 = helpers.create_alert(db=db)
    initial_alert3_version = alert_tree3.node.version

    assert alert_tree1.node.description is None
    assert alert_tree2.node.event_time != parse("2022-01-01T00:00:00+00:00")
    assert alert_tree3.node.instructions is None

    # Update all the alerts at once
    update_data = [
        {"description": "updated_description", "uuid": str(alert_tree1.node_uuid)},
        {"event_time": "2022-01-01 00:00:00", "uuid": str(alert_tree2.node_uuid)},
        {"instructions": "updated_instructions", "uuid": str(alert_tree3.node_uuid)},
    ]
    update = client_valid_access_token.patch("/api/alert/", json=update_data)
    assert update.status_code == status.HTTP_204_NO_CONTENT

    assert alert_tree1.node.description == "updated_description"
    assert alert_tree1.node.version != initial_alert1_version

    assert alert_tree2.node.event_time == parse("2022-01-01T00:00:00+00:00")
    assert alert_tree2.node.version != initial_alert2_version

    assert alert_tree3.node.instructions == "updated_instructions"
    assert alert_tree3.node.version != initial_alert3_version
