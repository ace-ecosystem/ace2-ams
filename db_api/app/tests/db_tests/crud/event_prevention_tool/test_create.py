from api_models.event_prevention_tool import EventPreventionToolCreate
from db import crud
from tests import factory


def test_create(db):
    queue = factory.queue.create_or_read(value="test_queue", db=db)

    obj = crud.event_prevention_tool.create_or_read(
        model=EventPreventionToolCreate(description="test description", value="test", queues=["test_queue"]),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.queues == [queue]
    assert obj.value == "test"


def test_create_duplicate(db):
    obj = crud.event_prevention_tool.create_or_read(
        model=EventPreventionToolCreate(value="test", queues=["external"]), db=db
    )

    obj2 = crud.event_prevention_tool.create_or_read(
        model=EventPreventionToolCreate(value="test", queues=["external"]), db=db
    )

    assert obj2.uuid == obj.uuid
