from db import crud
from tests import factory


def test_read_all(db):
    obj1 = factory.alert_disposition.create_or_read(value="test", rank=1, db=db)
    obj2 = factory.alert_disposition.create_or_read(value="test2", rank=2, db=db)

    result = crud.alert_disposition.read_all(db=db)
    assert len(result) == 2
    assert result[0].uuid == obj1.uuid
    assert result[1].uuid == obj2.uuid


def test_read_by_uuid(db):
    obj = factory.alert_disposition.create_or_read(value="test", rank=1, db=db)

    result = crud.alert_disposition.read_by_uuid(uuid=obj.uuid, db=db)
    assert result.uuid == obj.uuid


def test_read_by_value(db):
    obj = factory.alert_disposition.create_or_read(value="test", rank=1, db=db)

    result = crud.alert_disposition.read_by_value(value=obj.value, db=db)
    assert result.uuid == obj.uuid
