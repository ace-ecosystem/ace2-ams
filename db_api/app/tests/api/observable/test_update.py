import pytest
import uuid

from datetime import datetime
from dateutil.parser import parse
from fastapi import status

from tests.api.node import INVALID_LIST_STRING_VALUES, VALID_LIST_STRING_VALUES
from tests import factory


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
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/observable/{uuid.uuid4()}", json={key: value})
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
def test_update_invalid_node_fields(client, key, values):
    for value in values:
        update = client.patch(
            f"/api/observable/{uuid.uuid4()}",
            json={key: value},
        )
        assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in update.json()["detail"][0]["loc"]


def test_update_invalid_uuid(client):
    update = client.patch("/api/observable/1", json={"types": ["test_type"], "value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client, db):
    alert = factory.alert.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=alert.root_analysis, db=db
    )

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client.patch(f"/api/observable/{observable.uuid}", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_redirection_uuid(client, db):
    alert = factory.alert.create(db=db)
    observable_tree = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=alert.root_analysis, db=db
    )

    # Make sure you cannot update it to use a nonexistent redirection UUID
    update = client.patch(
        f"/api/observable/{observable_tree.uuid}",
        json={"redirection_uuid": str(uuid.uuid4())},
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key",
    [("directives"), ("tags"), ("threat_actors"), ("threats")],
)
def test_update_nonexistent_node_fields(client, db, key):
    alert = factory.alert.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=alert.root_analysis, db=db
    )

    # Make sure you cannot update it to use a nonexistent node field value
    update = client.patch(f"/api/observable/{observable.uuid}", json={key: ["abc"]})
    assert update.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in update.text


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/observable/{uuid.uuid4()}", json={"type": "test_type", "value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_type(client, db):
    alert = factory.alert.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    assert observable.type.value == "test_type"

    # Create a new observable type
    factory.observable_type.create_or_read(value="test_type2", db=db)

    # Update it
    update = client.patch(
        f"/api/observable/{observable.uuid}", json={"type": "test_type2", "history_username": "analyst"}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert observable.type.value == "test_type2"

    # Verify the history
    history = client.get(f"/api/observable/{observable.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "type"
    assert history.json()["items"][1]["diff"]["old_value"] == "test_type"
    assert history.json()["items"][1]["diff"]["new_value"] == "test_type2"
    assert history.json()["items"][1]["snapshot"]["type"]["value"] == "test_type2"


def test_update_redirection_uuid(client, db):
    alert = factory.alert.create(db=db)
    obs1 = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    initial_observable_version = obs1.version
    assert obs1.redirection is None

    # Create a second observable to use for redirection
    obs2 = factory.observable.create_or_read(
        type="test_type", value="test2", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )

    # Update the redirection UUID
    update = client.patch(
        f"/api/observable/{obs1.uuid}",
        json={"redirection_uuid": str(obs2.uuid), "history_username": "analyst"},
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert obs1.redirection_uuid == obs2.uuid
    assert obs1.version != initial_observable_version

    # Verify the history
    history = client.get(f"/api/observable/{obs1.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == "redirection_uuid"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] == str(obs2.uuid)
    assert history.json()["items"][1]["snapshot"]["redirection"]["uuid"] == str(obs2.uuid)

    # Set it back to None
    update = client.patch(
        f"/api/observable/{obs1.uuid}", json={"redirection_uuid": None, "history_username": "analyst"}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert obs1.redirection is None

    # Verify the history
    history = client.get(f"/api/observable/{obs1.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["field"] == "redirection_uuid"
    assert history.json()["items"][2]["diff"]["old_value"] == str(obs2.uuid)
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["snapshot"]["redirection"] is None


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("directives", VALID_LIST_STRING_VALUES, factory.node_directive.create_or_read),
        ("tags", VALID_LIST_STRING_VALUES, factory.node_tag.create_or_read),
        ("threat_actors", VALID_LIST_STRING_VALUES, factory.node_threat_actor.create_or_read),
        ("threats", VALID_LIST_STRING_VALUES, factory.node_threat.create_or_read),
    ],
)
def test_update_valid_node_fields(client, db, key, value_lists, helper_create_func):
    alert = factory.alert.create(db=db)

    for i in range(len(value_lists)):
        value_list = value_lists[i]

        observable = factory.observable.create_or_read(
            type="test_type",
            value=f"test{i}",
            directives=["remove_me"],
            tags=["remove_me"],
            threat_actors=["remove_me"],
            threats=["remove_me"],
            parent_analysis=alert.root_analysis,
            db=db,
            history_username="analyst",
        )
        initial_observable_version = observable.version

        for value in value_list:
            helper_create_func(value=value, db=db)

        # Update the observable
        update = client.patch(
            f"/api/observable/{observable.uuid}", json={key: value_list, "history_username": "analyst"}
        )
        assert update.status_code == status.HTTP_204_NO_CONTENT
        assert len(getattr(observable, key)) == len(set(value_list))
        assert observable.version != initial_observable_version

        # Verify the history
        if value_list:
            history = client.get(f"/api/observable/{observable.uuid}/history")
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
def test_update(client, db, key, initial_value, updated_value):
    alert = factory.alert.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )

    # Set the initial value
    if key == "expires_on" and initial_value:
        setattr(observable, key, datetime.utcfromtimestamp(initial_value))
    else:
        setattr(observable, key, initial_value)

    # Update it
    update = client.patch(
        f"/api/observable/{observable.uuid}", json={key: updated_value, "history_username": "analyst"}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Verify the history
    history = client.get(f"/api/observable/{observable.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["field"] == key

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if key in ["expires_on", "time"]:
        if initial_value:
            assert history.json()["items"][1]["diff"]["old_value"] == parse("2021-01-01T00:00:00+00:00").isoformat()
        else:
            assert history.json()["items"][1]["diff"]["old_value"] is None

        if updated_value:
            assert getattr(observable, key) == parse("2022-01-01T00:00:00+00:00")
            assert history.json()["items"][1]["diff"]["new_value"] == parse("2022-01-01T00:00:00+00:00").isoformat()
        else:
            assert getattr(observable, key) is None
            assert history.json()["items"][1]["diff"]["new_value"] is None
    else:
        assert getattr(observable, key) == updated_value
        assert history.json()["items"][1]["diff"]["old_value"] == initial_value
        assert history.json()["items"][1]["diff"]["new_value"] == updated_value

    assert history.json()["items"][1]["snapshot"]["value"] == observable.value
