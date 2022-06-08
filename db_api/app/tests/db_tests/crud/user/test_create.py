import json

from api_models.user import UserCreate
from db import crud
from tests import factory


#
# VALID TESTS
#


def test_create(db):
    factory.queue.create_or_read(value="test_queue", db=db)
    factory.user_role.create_or_read(value="test_role", db=db)

    obj = crud.user.create_or_read(
        model=UserCreate(
            default_alert_queue="test_queue",
            default_event_queue="test_queue",
            display_name="analyst2",
            email="analyst2@localhost.localdomain",
            enabled=True,
            history_username="analyst",
            password="asdfasdf",
            roles=["test_role"],
            timezone="UTC",
            training=False,
            username="analyst2",
        ),
        db=db,
    )

    assert obj.default_alert_queue.value == "test_queue"
    assert obj.default_event_queue.value == "test_queue"
    assert obj.display_name == "analyst2"
    assert obj.email == "analyst2@localhost.localdomain"
    assert obj.enabled is True
    assert len(obj.history) == 1
    assert len(obj.roles) == 1
    assert obj.roles[0].value == "test_role"
    assert obj.timezone == "UTC"
    assert obj.training is False
    assert obj.username == "analyst2"


def test_create_duplicate(db):
    factory.queue.create_or_read(value="test_queue", db=db)
    factory.user_role.create_or_read(value="test_role", db=db)

    obj = crud.user.create_or_read(
        model=UserCreate(
            default_alert_queue="test_queue",
            default_event_queue="test_queue",
            display_name="analyst",
            email="analyst@localhost.localdomain",
            password="asdfasdf",
            roles=["test_role"],
            username="analyst",
        ),
        db=db,
    )

    obj2 = crud.user.create_or_read(
        model=UserCreate(
            default_alert_queue="test_queue",
            default_event_queue="test_queue",
            display_name="analyst2",
            email="analyst@localhost.localdomain",
            password="asdfasdf",
            roles=["test_role"],
            username="analyst",
        ),
        db=db,
    )

    assert obj2.uuid == obj.uuid
