import pytest

from api_models.user import UserUpdate
from core.auth import verify_password
from db import crud
from tests import factory


#
# INVALID TESTS
#


def test_update_conflicting_username(db):
    user1 = factory.user.create_or_read(username="user1", db=db)
    user2 = factory.user.create_or_read(username="user2", db=db)
    assert crud.user.update(uuid=user2.uuid, model=UserUpdate(username=user1.username), db=db) is False


#
# VALID TESTS
#


def test_update_valid_alert_queue(db):
    # Create a user
    obj = factory.user.create_or_read(username="janedoe", alert_queue="test_queue", db=db, history_username="analyst")
    assert obj.default_alert_queue.value == "test_queue"

    # Create the new alert queue
    factory.queue.create_or_read(value="test_queue2", db=db)

    # Update it
    crud.user.update(
        uuid=obj.uuid, model=UserUpdate(default_alert_queue="test_queue2", history_username="analyst"), db=db
    )
    assert obj.default_alert_queue.value == "test_queue2"

    # Verify the history
    assert len(obj.history) == 2
    assert obj.history[1].action == "UPDATE"
    assert obj.history[1].action_by.username == "analyst"
    assert obj.history[1].field == "default_alert_queue"
    assert obj.history[1].diff["old_value"] == "test_queue"
    assert obj.history[1].diff["new_value"] == "test_queue2"
    assert obj.history[1].snapshot["default_alert_queue"]["value"] == "test_queue2"


def test_update_valid_event_queue(db):
    # Create a user
    obj = factory.user.create_or_read(username="janedoe", event_queue="test_queue", db=db, history_username="analyst")
    assert obj.default_event_queue.value == "test_queue"

    # Create the new event queue
    factory.queue.create_or_read(value="test_queue2", db=db)

    # Update it
    crud.user.update(
        uuid=obj.uuid, model=UserUpdate(default_event_queue="test_queue2", history_username="analyst"), db=db
    )
    assert obj.default_event_queue.value == "test_queue2"

    # Verify the history
    assert len(obj.history) == 2
    assert obj.history[1].action == "UPDATE"
    assert obj.history[1].action_by.username == "analyst"
    assert obj.history[1].field == "default_event_queue"
    assert obj.history[1].diff["old_value"] == "test_queue"
    assert obj.history[1].diff["new_value"] == "test_queue2"
    assert obj.history[1].snapshot["default_event_queue"]["value"] == "test_queue2"


@pytest.mark.parametrize(
    "values",
    [
        (["new_role"]),
        (["new_role1", "new_role2"]),
    ],
)
def test_update_valid_roles(db, values):
    # Create a user
    initial_roles = ["test_role1", "test_role2", "test_role3"]
    obj = factory.user.create_or_read(username="janedoe", roles=initial_roles, db=db, history_username="analyst")
    assert len(obj.roles) == len(initial_roles)

    # Create the new user roles
    for value in values:
        factory.user_role.create_or_read(value=value, db=db)

    # Update it
    crud.user.update(uuid=obj.uuid, model=UserUpdate(roles=values, history_username="analyst"), db=db)
    assert len(obj.roles) == len(values)

    # Verify the history
    assert len(obj.history) == 2
    assert obj.history[1].action == "UPDATE"
    assert obj.history[1].action_by.username == "analyst"
    assert obj.history[1].field == "roles"
    assert obj.history[1].diff["old_value"] is None
    assert obj.history[1].diff["new_value"] is None
    assert obj.history[1].diff["added_to_list"] == values
    assert obj.history[1].diff["removed_from_list"] == initial_roles
    assert len(obj.history[1].snapshot["roles"]) == len(set(values))


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("display_name", "John Doe", "Johnathan Doe"),
        ("display_name", "John Doe", "John Doe"),
        ("email", "john@test.com", "johnathan@test.com"),
        ("email", "john@test.com", "john@test.com"),
        ("enabled", True, False),
        ("enabled", False, True),
        ("timezone", "UTC", "America/New_York"),
        ("timezone", "UTC", "UTC"),
        ("training", True, False),
        ("training", False, True),
        ("username", "janedoe", "johnathandoe"),
        ("username", "janedoe", "janedoe"),
    ],
)
def test_update(db, key, initial_value, updated_value):
    # Create a user
    obj = factory.user.create_or_read(username="janedoe", db=db, history_username="analyst")

    # Set the initial value
    setattr(obj, key, initial_value)

    # Update it
    crud.user.update(uuid=obj.uuid, model=UserUpdate(history_username="analyst", **{key: updated_value}), db=db)
    assert getattr(obj, key) == updated_value

    # Verify the history
    assert len(obj.history) == 2
    assert obj.history[1].action == "UPDATE"
    assert obj.history[1].action_by.username == "analyst"
    assert obj.history[1].field == key
    assert obj.history[1].diff["old_value"] == initial_value
    assert obj.history[1].diff["new_value"] == updated_value
    assert obj.history[1].snapshot["username"] == obj.username


@pytest.mark.parametrize(
    "initial_value,updated_value",
    [
        ("abcd1234", "wxyz6789"),
        ("abcd1234", "abcd1234"),
    ],
)
def test_update_password(db, initial_value, updated_value):
    # Create a user
    obj = factory.user.create_or_read(username="janedoe", password=initial_value, db=db, history_username="analyst")
    initial_password_hash = obj.password

    # Make sure the initial password validates against its hash
    assert verify_password(initial_value, initial_password_hash) is True

    # Update it
    crud.user.update(uuid=obj.uuid, model=UserUpdate(password=updated_value, history_username="analyst"), db=db)
    assert obj.password != initial_password_hash
    assert verify_password(updated_value, obj.password) is True

    # Verify the history
    assert len(obj.history) == 2
    assert obj.history[1].action == "UPDATE"
    assert obj.history[1].action_by.username == "analyst"
    assert obj.history[1].field == "password"
    assert obj.history[1].diff["old_value"] is None
    assert obj.history[1].diff["new_value"] is None
    assert obj.history[1].snapshot["username"] == "janedoe"
