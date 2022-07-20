from api_models.analysis_status import AnalysisStatusCreate
from db import crud


def test_create(db):
    obj = crud.analysis_status.create_or_read(model=AnalysisStatusCreate(value="test value"), db=db)

    assert obj.description is None
    assert obj.value == "test value"


def test_create_duplicate_value(db):
    obj1 = crud.analysis_status.create_or_read(model=AnalysisStatusCreate(value="test"), db=db)
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.analysis_status.create_or_read(model=AnalysisStatusCreate(value=obj1.value), db=db)
    assert obj2.description == obj1.description
    assert obj2.uuid == obj1.uuid
    assert obj2.value == obj1.value
