from api_models.metadata_sort import MetadataSortCreate
from db import crud


def test_create(db):
    obj = crud.metadata_sort.create_or_read(model=MetadataSortCreate(description="test description", value=1), db=db)

    assert obj.description == "test description"
    assert obj.value == 1


def test_create_duplicate_value(db):
    obj1 = crud.metadata_sort.create_or_read(model=MetadataSortCreate(value=1), db=db)
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.metadata_sort.create_or_read(model=MetadataSortCreate(value=obj1.value), db=db)
    assert obj2.description == obj1.description
    assert obj2.uuid == obj1.uuid
    assert obj2.value == obj1.value
