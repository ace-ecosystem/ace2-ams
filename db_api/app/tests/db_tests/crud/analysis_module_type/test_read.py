from db import crud
from tests import factory


def test_read_all(db):
    factory.analysis_module_type.create_or_read(value="module1", db=db)
    factory.analysis_module_type.create_or_read(value="module2", db=db)

    result = crud.analysis_module_type.read_all(db=db)
    assert len(result) == 2
    assert result[0].value == "module1"
    assert result[1].value == "module2"


def test_read_by_value_latest_version(db):
    factory.analysis_module_type.create_or_read(value="module", version="1.0.0", db=db)
    obj2 = factory.analysis_module_type.create_or_read(value="module", version="2.0.0", db=db)

    result = crud.analysis_module_type.read_by_value_latest_version(value="module", db=db)
    assert result.uuid == obj2.uuid
