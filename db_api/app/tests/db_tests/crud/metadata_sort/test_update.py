from api_models.metadata_sort import MetadataSortUpdate
from db import crud
from tests import factory


def test_update(db):
    obj = factory.metadata_sort.create_or_read(value=1, db=db)

    assert obj.description is None
    assert obj.value == 1

    crud.metadata_sort.update(
        uuid=obj.uuid,
        model=MetadataSortUpdate(description="test description", value=2),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.value == 2


def test_update_duplicate_value(db):
    obj1 = factory.metadata_sort.create_or_read(value=1, db=db)
    obj2 = factory.metadata_sort.create_or_read(value=2, db=db)

    result = crud.metadata_sort.update(uuid=obj2.uuid, model=MetadataSortUpdate(value=obj1.value), db=db)
    assert result is False
