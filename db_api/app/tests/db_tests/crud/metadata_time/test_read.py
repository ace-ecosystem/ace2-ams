from db import crud
from tests import factory


def test_read_by_uuid(db):
    obj = factory.metadata_time.create_or_read(value=crud.helpers.utcnow(), db=db)

    result = crud.metadata_time.read_by_uuid(uuid=obj.uuid, db=db)
    assert result.uuid == obj.uuid


def test_read_by_value(db):
    obj = factory.metadata_time.create_or_read(value=crud.helpers.utcnow(), db=db)

    result = crud.metadata_time.read_by_value(value=obj.value, db=db)
    assert result.uuid == obj.uuid
