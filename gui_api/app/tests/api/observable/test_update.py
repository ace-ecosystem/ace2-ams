import pytest
import uuid

from datetime import datetime
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
        ("context", 123),
        ("context", ""),
        ("expires_on", ""),
        ("expires_on", "Monday"),
        ("expires_on", "2022-01-01"),
        ("for_detection", 123),
        ("for_detection", None),
        ("for_detection", "True"),
        ("redirection_uuid", 123),
        ("redirection_uuid", ""),
        ("redirection_uuid", "abc"),
        ("time", None),
        ("time", ""),
        ("time", "Monday"),
        ("time", "2022-01-01"),
        ("type", 123),
        ("type", None),
        ("type", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/observable/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(update.json()["detail"]) == 1
    assert key in update.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key,values",
    [
        ("directives", INVALID_LIST_STRING_VALUES),
        ("tags", INVALID_LIST_STRING_VALUES),
        ("threat_actors", INVALID_LIST_STRING_VALUES),
        ("threats", INVALID_LIST_STRING_VALUES),
    ],
)
def test_update_invalid_node_fields(client_valid_access_token, key, values):
    for value in values:
        update = client_valid_access_token.patch(
            f"/api/observable/{uuid.uuid4()}",
            json={key: value},
        )
        assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in update.json()["detail"][0]["loc"]


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/observable/1", json={"types": ["test_type"], "value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test", parent_tree=alert_tree, db=db)

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client_valid_access_token.patch(
        f"/api/observable/{observable_tree.node.uuid}", json={"version": str(uuid.uuid4())}
    )
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_duplicate_type_value(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    observable_tree1 = helpers.create_observable(type="test_type", value="test", parent_tree=alert_tree, db=db)
    observable_tree2 = helpers.create_observable(type="test_type", value="test2", parent_tree=alert_tree, db=db)

    # Ensure you cannot update an observable to have a duplicate type+value combination
    update = client_valid_access_token.patch(
        f"/api/observable/{observable_tree2.node.uuid}", json={"value": observable_tree1.node.value}
    )
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_redirection_uuid(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test", parent_tree=alert_tree, db=db)

    # Make sure you cannot update it to use a nonexistent redirection UUID
    update = client_valid_access_token.patch(
        f"/api/observable/{observable_tree.node.uuid}",
        json={"redirection_uuid": str(uuid.uuid4())},
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key",
    [("directives"), ("tags"), ("threat_actors"), ("threats")],
)
def test_update_nonexistent_node_fields(client_valid_access_token, db, key):
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test", parent_tree=alert_tree, db=db)

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch(f"/api/observable/{observable_tree.node.uuid}", json={key: ["abc"]})
    assert update.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in update.text


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(
        f"/api/observable/{uuid.uuid4()}", json={"type": "test_type", "value": "test"}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_type(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test", parent_tree=alert_tree, db=db)
    assert observable_tree.node.type.value == "test_type"

    # Create a new observable type
    helpers.create_observable_type(value="test_type2", db=db)

    # Update it
    update = client_valid_access_token.patch(
        f"/api/observable/{observable_tree.node.uuid}", json={"type": "test_type2"}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert observable_tree.node.type.value == "test_type2"

    # Verify the history
    history = client_valid_access_token.get(f"/api/observable/{observable_tree.node_uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "type"
    assert history.json()["items"][1]["diff"]["old_value"] == "test_type"
    assert history.json()["items"][1]["diff"]["new_value"] == "test_type2"
    assert history.json()["items"][1]["snapshot"]["type"]["value"] == "test_type2"


def test_update_redirection_uuid(client_valid_access_token, db):
    alert_tree = helpers.create_alert(db=db)
    observable_tree1 = helpers.create_observable(type="test_type", value="test", parent_tree=alert_tree, db=db)
    initial_observable_version = observable_tree1.node.version
    assert observable_tree1.node.redirection is None

    # Create a second observable to use for redirection
    observable_tree2 = helpers.create_observable(type="test_type", value="test2", parent_tree=alert_tree, db=db)

    # Update the redirection UUID
    update = client_valid_access_token.patch(
        f"/api/observable/{observable_tree1.node.uuid}", json={"redirection_uuid": str(observable_tree2.node.uuid)}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert observable_tree1.node.redirection_uuid == observable_tree2.node.uuid
    assert observable_tree1.node.version != initial_observable_version

    # Verify the history
    history = client_valid_access_token.get(f"/api/observable/{observable_tree1.node_uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "redirection_uuid"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == str(observable_tree2.node.uuid)
    assert history.json()["items"][1]["snapshot"]["redirection_uuid"] == str(observable_tree2.node.uuid)

    # Set it back to None
    update = client_valid_access_token.patch(
        f"/api/observable/{observable_tree1.node.uuid}", json={"redirection_uuid": None}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert observable_tree1.node.redirection is None

    # Verify the history
    history = client_valid_access_token.get(f"/api/observable/{observable_tree1.node_uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "redirection_uuid"
    assert history.json()["items"][2]["diff"]["old_value"] == str(observable_tree2.node.uuid)
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["redirection_uuid"] is None


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("directives", VALID_LIST_STRING_VALUES, helpers.create_node_directive),
        ("tags", VALID_LIST_STRING_VALUES, helpers.create_node_tag),
        ("threat_actors", VALID_LIST_STRING_VALUES, helpers.create_node_threat_actor),
        ("threats", VALID_LIST_STRING_VALUES, helpers.create_node_threat),
    ],
)
def test_update_valid_node_fields(client_valid_access_token, db, key, value_lists, helper_create_func):
    for i in range(len(value_lists)):
        value_list = value_lists[i]

        alert_tree = helpers.create_alert(db=db)
        observable_tree = helpers.create_observable(
            type="test_type",
            value=f"test{i}",
            directives=["remove_me"],
            tags=["remove_me"],
            threat_actors=["remove_me"],
            threats=["remove_me"],
            parent_tree=alert_tree,
            db=db,
        )
        initial_observable_version = observable_tree.node.version

        for value in value_list:
            helper_create_func(value=value, db=db)

        # Update the observable
        update = client_valid_access_token.patch(f"/api/observable/{observable_tree.node.uuid}", json={key: value_list})
        assert update.status_code == status.HTTP_204_NO_CONTENT
        assert len(getattr(observable_tree.node, key)) == len(set(value_list))
        assert observable_tree.node.version != initial_observable_version

        # Verify the history
        if value_list:
            history = client_valid_access_token.get(f"/api/observable/{observable_tree.node_uuid}/history")
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
        ("context", None, "test"),
        ("context", "test", None),
        ("context", "test", "test"),
        ("expires_on", 1609459200, 1640995200),
        ("expires_on", None, 1640995200),
        ("expires_on", None, "2022-01-01T00:00:00Z"),
        ("expires_on", None, "2022-01-01 00:00:00"),
        ("expires_on", None, "2022-01-01 00:00:00.000000"),
        ("expires_on", None, "2021-12-31 19:00:00-05:00"),
        ("expires_on", 1609459200, None),
        ("for_detection", True, False),
        ("for_detection", True, True),
        ("time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client_valid_access_token, db, key, initial_value, updated_value):
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test", parent_tree=alert_tree, db=db)

    # Set the initial value
    if key == "expires_on" and initial_value:
        setattr(observable_tree.node, key, datetime.utcfromtimestamp(initial_value))
    else:
        setattr(observable_tree.node, key, initial_value)

    # Update it
    update = client_valid_access_token.patch(f"/api/observable/{observable_tree.node_uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Verify the history
    history = client_valid_access_token.get(f"/api/observable/{observable_tree.node_uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == key

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if key == "expires_on" or key == "time":
        if initial_value:
            assert history.json()["items"][1]["diff"]["old_value"] == parse("2021-01-01T00:00:00+00:00").isoformat()
        else:
            assert history.json()["items"][1]["diff"]["old_value"] is None

        if updated_value:
            assert getattr(observable_tree.node, key) == parse("2022-01-01T00:00:00+00:00")
            assert history.json()["items"][1]["diff"]["new_value"] == parse("2022-01-01T00:00:00+00:00").isoformat()
        else:
            assert getattr(observable_tree.node, key) is None
            assert history.json()["items"][1]["diff"]["new_value"] is None
    else:
        assert getattr(observable_tree.node, key) == updated_value
        assert history.json()["items"][1]["diff"]["old_value"] == initial_value
        assert history.json()["items"][1]["diff"]["new_value"] == updated_value

    assert history.json()["items"][1]["snapshot"]["value"] == observable_tree.node.value
