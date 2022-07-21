from db import crud
from tests import factory


def test_read_all(db):
    obj1 = factory.metadata_sort.create_or_read(value=1, db=db)
    obj2 = factory.metadata_sort.create_or_read(value=2, db=db)

    result = crud.metadata_sort.read_all(db=db)
    assert len(result) == 2
    assert result[0].uuid == obj1.uuid
    assert result[1].uuid == obj2.uuid


def test_read_by_uuid(db):
    obj = factory.metadata_sort.create_or_read(value=1, db=db)

    result = crud.metadata_sort.read_by_uuid(uuid=obj.uuid, db=db)
    assert result.uuid == obj.uuid


def test_read_by_value(db):
    obj = factory.metadata_sort.create_or_read(value=1, db=db)

    result = crud.metadata_sort.read_by_value(value=obj.value, db=db)
    assert result.uuid == obj.uuid
