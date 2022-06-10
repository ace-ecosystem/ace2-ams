from api_models.event_type import EventTypeCreate
from db import crud
from tests import factory


def test_create(db):
    queue = factory.queue.create_or_read(value="test_queue", db=db)

    obj = crud.event_type.create_or_read(
        model=EventTypeCreate(description="test description", value="test", queues=["test_queue"]),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.queues == [queue]
    assert obj.value == "test"


def test_create_duplicate(db):
    obj = crud.event_type.create_or_read(model=EventTypeCreate(value="test", queues=["external"]), db=db)
    obj2 = crud.event_type.create_or_read(model=EventTypeCreate(value="test", queues=["external"]), db=db)

    assert obj2.uuid == obj.uuid
