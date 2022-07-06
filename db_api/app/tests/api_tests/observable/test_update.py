import pytest
import uuid

from datetime import datetime
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
        ("context", 123),
        ("context", ""),
        ("expires_on", ""),
        ("expires_on", "Monday"),
        ("expires_on", "2022-01-01"),
        ("for_detection", 123),
        ("for_detection", None),
        ("for_detection", "True"),
        ("type", 123),
        ("type", None),
        ("type", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
        ("whitelisted", 123),
        ("whitelisted", None),
        ("whitelisted", "True"),
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
        ("tags", INVALID_LIST_STRING_VALUES),
    ],
)
def test_update_invalid_list_fields(client, key, values):
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
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=submission.root_analysis, db=db
    )

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client.patch(f"/api/observable/{observable.uuid}", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_duplicate_type_value(client, db):
    submission = factory.submission.create(db=db)
    observable1 = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=submission.root_analysis, db=db
    )
    observable2 = factory.observable.create_or_read(
        type="test_type", value="test2", parent_analysis=submission.root_analysis, db=db
    )

    # Ensure you cannot update an observable to have a duplicate type+value combination
    update = client.patch(f"/api/observable/{observable2.uuid}", json={"value": observable1.value})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "key",
    [("tags")],
)
def test_update_nonexistent_list_fields(client, db, key):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=submission.root_analysis, db=db
    )

    # Make sure you cannot update it to use a nonexistent list field value
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
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=submission.root_analysis, db=db, history_username="analyst"
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


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("tags", VALID_LIST_STRING_VALUES, factory.metadata_tag.create_or_read),
    ],
)
def test_update_valid_list_fields(client, db, key, value_lists, helper_create_func):
    submission = factory.submission.create(db=db)

    for i in range(len(value_lists)):
        value_list = value_lists[i]

        observable = factory.observable.create_or_read(
            type="test_type",
            value=f"test{i}",
            tags=["remove_me"],
            parent_analysis=submission.root_analysis,
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
        ("value", "test", "test2"),
        ("value", "test", "test"),
        ("whitelisted", True, False),
        ("whitelisted", True, True),
    ],
)
def test_update(client, db, key, initial_value, updated_value):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=submission.root_analysis, db=db, history_username="analyst"
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
    if key == "expires_on":
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
