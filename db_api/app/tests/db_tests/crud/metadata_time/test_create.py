from api_models.metadata_time import MetadataTimeCreate
from db import crud


def test_create(db):
    now = crud.helpers.utcnow()
    obj = crud.metadata_time.create_or_read(model=MetadataTimeCreate(description="test description", value=now), db=db)

    assert obj.description == "test description"
    assert obj.value == now


def test_create_duplicate_value(db):
    now = crud.helpers.utcnow()
    obj1 = crud.metadata_time.create_or_read(model=MetadataTimeCreate(value=now), db=db)
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.metadata_time.create_or_read(model=MetadataTimeCreate(value=obj1.value), db=db)
    assert obj2.description == obj1.description
    assert obj2.uuid == obj1.uuid
    assert obj2.value == obj1.value
