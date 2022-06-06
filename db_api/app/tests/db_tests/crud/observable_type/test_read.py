from db import crud
from tests import factory


def test_read_all(db):
    obj1 = factory.observable_type.create_or_read(value="test", db=db)
    obj2 = factory.observable_type.create_or_read(value="test2", db=db)

    result = crud.observable_type.read_all(db=db)
    assert len(result) == 2
    assert result[0].uuid == obj1.uuid
    assert result[1].uuid == obj2.uuid


def test_read_by_uuid(db):
    obj = factory.observable_type.create_or_read(value="test", db=db)

    result = crud.observable_type.read_by_uuid(uuid=obj.uuid, db=db)
    assert result.uuid == obj.uuid


def test_read_by_value(db):
    obj = factory.observable_type.create_or_read(value="test", db=db)

    result = crud.observable_type.read_by_value(value=obj.value, db=db)
    assert result.uuid == obj.uuid
