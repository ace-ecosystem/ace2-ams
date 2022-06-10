from db import crud
from tests import factory


def test_read_all(db):
    obj1 = factory.queue.create_or_read(value="test", db=db)
    obj2 = factory.queue.create_or_read(value="test2", db=db)

    result = crud.queue.read_all(db=db)
    # There is a default "external" queue, so that will be the first element
    assert len(result) == 3
    assert result[0].value == "external"
    assert result[1].uuid == obj1.uuid
    assert result[2].uuid == obj2.uuid


def test_read_by_uuid(db):
    obj = factory.queue.create_or_read(value="test", db=db)

    result = crud.queue.read_by_uuid(uuid=obj.uuid, db=db)
    assert result.uuid == obj.uuid


def test_read_by_value(db):
    obj = factory.queue.create_or_read(value="test", db=db)

    result = crud.queue.read_by_value(value=obj.value, db=db)
    assert result.uuid == obj.uuid
