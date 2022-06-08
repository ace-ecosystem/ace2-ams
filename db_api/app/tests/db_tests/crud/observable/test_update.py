import pytest

from datetime import timedelta
from uuid import uuid4

from api_models.observable import ObservableUpdate
from db import crud
from exceptions.db import VersionMismatch
from tests import factory
from tests.api.node import VALID_LIST_STRING_VALUES


#
# INVALID TESTS
#


def test_update_duplicate_type_value(db):
    # Create two observables
    submission = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, history_username="analyst", db=db
    )
    obs2 = factory.observable.create_or_read(
        type="type2", value="value", parent_analysis=submission.root_analysis, history_username="analyst", db=db
    )

    # Try to update the second one to the first type
    result = crud.observable.update(
        uuid=obs2.uuid, model=ObservableUpdate(type=obs1.type.value, history_username="analyst"), db=db
    )
    assert result is False


def test_update_version_mismatch(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, history_username="analyst", db=db
    )

    with pytest.raises(VersionMismatch):
        crud.observable.update(uuid=observable.uuid, model=ObservableUpdate(for_detection=True, version=uuid4()), db=db)


#
# VALID TESTS
#


NOW = crud.helpers.utcnow()
UPDATED_TIME = NOW + timedelta(days=1)


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("context", None, "test"),
        ("context", "test", None),
        ("context", "test", "test"),
        ("expires_on", NOW, None),
        ("expires_on", NOW, UPDATED_TIME),
        ("for_detection", True, False),
        ("for_detection", True, True),
        ("time", NOW, UPDATED_TIME),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(db, key, initial_value, updated_value):
    # Create an observable
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, history_username="analyst", db=db
    )
    initial_observable_version = observable.version

    # Set the initial value
    setattr(observable, key, initial_value)

    # Update it
    update_model = ObservableUpdate(history_username="analyst")
    setattr(update_model, key, updated_value)
    crud.observable.update(uuid=observable.uuid, model=update_model, db=db)
    assert observable.version != initial_observable_version

    # Verify the history
    assert len(observable.history) == 2
    assert observable.history[1].action == "UPDATE"
    assert observable.history[1].action_by.username == "analyst"
    assert observable.history[1].field == key

    old_value = initial_value
    if key in ["expires_on", "time"]:
        old_value = initial_value.isoformat()

    new_value = updated_value
    if key in ["expires_on", "time"] and updated_value:
        new_value = updated_value.isoformat()

    assert observable.history[1].diff["old_value"] == old_value
    assert observable.history[1].diff["new_value"] == new_value


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("directives", VALID_LIST_STRING_VALUES, factory.node_directive.create_or_read),
        ("tags", VALID_LIST_STRING_VALUES, factory.node_tag.create_or_read),
        ("threat_actors", VALID_LIST_STRING_VALUES, factory.node_threat_actor.create_or_read),
        ("threats", VALID_LIST_STRING_VALUES, factory.node_threat.create_or_read),
    ],
)
def test_update_node_fields(db, key, value_lists, helper_create_func):
    submission = factory.submission.create(db=db)

    for i in range(len(value_lists)):
        value_list = value_lists[i]

        observable = factory.observable.create_or_read(
            type="test_type",
            value=f"test{i}",
            directives=["remove_me"],
            tags=["remove_me"],
            threat_actors=["remove_me"],
            threats=["remove_me"],
            parent_analysis=submission.root_analysis,
            db=db,
            history_username="analyst",
        )
        initial_observable_version = observable.version

        for value in value_list:
            helper_create_func(value=value, db=db)

        # Update the observable
        update_model = ObservableUpdate(history_username="analyst")
        setattr(update_model, key, value_list)
        crud.observable.update(uuid=observable.uuid, model=update_model, db=db)
        assert len(getattr(observable, key)) == len(set(value_list))
        assert observable.version != initial_observable_version

        # Verify the history
        if value_list:
            assert len(observable.history) == 2
            assert observable.history[1].action == "UPDATE"
            assert observable.history[1].action_by.username == "analyst"
            assert observable.history[1].field == key
            assert observable.history[1].diff["old_value"] is None
            assert observable.history[1].diff["new_value"] is None
            assert observable.history[1].diff["added_to_list"] == sorted(set(value_list))
            assert observable.history[1].diff["removed_from_list"] == ["remove_me"]
            assert len(observable.history[1].snapshot[key]) == len(set(value_list))


def test_update_redirection_uuid(db):
    submission = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=submission.root_analysis, db=db, history_username="analyst"
    )
    initial_observable_version = obs1.version
    assert obs1.redirection is None

    # Create a second observable to use for redirection
    obs2 = factory.observable.create_or_read(
        type="test_type", value="test2", parent_analysis=submission.root_analysis, db=db, history_username="analyst"
    )

    # Update the redirection UUID
    crud.observable.update(
        uuid=obs1.uuid, model=ObservableUpdate(redirection_uuid=obs2.uuid, history_username="analyst"), db=db
    )
    assert obs1.redirection_uuid == obs2.uuid
    assert obs1.version != initial_observable_version

    # Verify the history
    assert len(obs1.history) == 2
    assert obs1.history[1].action == "UPDATE"
    assert obs1.history[1].action_by.username == "analyst"
    assert obs1.history[1].field == "redirection_uuid"
    assert obs1.history[1].diff["old_value"] is None
    assert obs1.history[1].diff["new_value"] == str(obs2.uuid)
    assert obs1.history[1].snapshot["redirection"]["uuid"] == str(obs2.uuid)

    # Set it back to None
    crud.observable.update(
        uuid=obs1.uuid, model=ObservableUpdate(redirection_uuid=None, history_username="analyst"), db=db
    )
    assert obs1.redirection is None

    # Verify the history
    assert len(obs1.history) == 3
    assert obs1.history[2].action == "UPDATE"
    assert obs1.history[2].action_by.username == "analyst"
    assert obs1.history[2].field == "redirection_uuid"
    assert obs1.history[2].diff["old_value"] == str(obs2.uuid)
    assert obs1.history[2].diff["new_value"] is None
    assert obs1.history[2].snapshot["redirection"] is None


def test_update_type(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test", parent_analysis=submission.root_analysis, db=db, history_username="analyst"
    )
    assert observable.type.value == "test_type"

    # Create a new observable type
    factory.observable_type.create_or_read(value="test_type2", db=db)

    # Update it
    crud.observable.update(
        uuid=observable.uuid, model=ObservableUpdate(type="test_type2", history_username="analyst"), db=db
    )
    assert observable.type.value == "test_type2"

    # Verify the history
    assert len(observable.history) == 2
    assert observable.history[1].action == "UPDATE"
    assert observable.history[1].action_by.username == "analyst"
    assert observable.history[1].field == "type"
    assert observable.history[1].diff["old_value"] == "test_type"
    assert observable.history[1].diff["new_value"] == "test_type2"
    assert observable.history[1].snapshot["type"]["value"] == "test_type2"
