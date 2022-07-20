from db import crud
from tests import factory


def test_read_all(db):
    # conftest automatically creates two analysis status objects since they are required for creating analyses
    result = crud.analysis_status.read_all(db=db)
    assert len(result) == 2
    assert any(s.value == "complete" for s in result)
    assert any(s.value == "running" for s in result)


def test_read_by_uuid(db):
    obj = factory.analysis_status.create_or_read(value="test", db=db)

    result = crud.analysis_status.read_by_uuid(uuid=obj.uuid, db=db)
    assert result.uuid == obj.uuid


def test_read_by_value(db):
    obj = factory.analysis_status.create_or_read(value="test", db=db)

    result = crud.analysis_status.read_by_value(value=obj.value, db=db)
    assert result.uuid == obj.uuid
