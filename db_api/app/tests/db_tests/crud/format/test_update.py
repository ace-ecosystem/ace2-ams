from api_models.format import FormatUpdate
from db import crud
from tests import factory


def test_update(db):
    obj = factory.format.create_or_read(value="test", db=db)

    assert obj.description is None
    assert obj.value == "test"

    crud.format.update(
        uuid=obj.uuid,
        model=FormatUpdate(description="test description", value="new value"),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.value == "new value"


def test_update_duplicate_value(db):
    obj1 = factory.format.create_or_read(value="test", db=db)
    obj2 = factory.format.create_or_read(value="test2", db=db)

    result = crud.format.update(uuid=obj2.uuid, model=FormatUpdate(value=obj1.value), db=db)
    assert result is False
