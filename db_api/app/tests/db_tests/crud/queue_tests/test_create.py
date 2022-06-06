from api_models.queue import QueueCreate
from db import crud


def test_create(db):
    obj = crud.queue.create_or_read(model=QueueCreate(value="test value"), db=db)

    assert obj.description is None
    assert obj.value == "test value"


def test_create_duplicate_value(db):
    obj1 = crud.queue.create_or_read(model=QueueCreate(value="test"), db=db)
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.queue.create_or_read(model=QueueCreate(value=obj1.value), db=db)
    assert obj2.description == obj1.description
    assert obj2.uuid == obj1.uuid
    assert obj2.value == obj1.value
