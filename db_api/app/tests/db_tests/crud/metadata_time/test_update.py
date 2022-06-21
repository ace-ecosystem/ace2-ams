from datetime import timedelta

from api_models.metadata_time import MetadataTimeUpdate
from db import crud
from tests import factory


def test_update(db):
    now = crud.helpers.utcnow()
    obj = factory.metadata_time.create_or_read(value=now, db=db)

    assert obj.description is None
    assert obj.value == now

    later = now + timedelta(seconds=5)
    crud.metadata_time.update(
        uuid=obj.uuid,
        model=MetadataTimeUpdate(description="test description", value=later),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.value == later


def test_update_duplicate_value(db):
    now = crud.helpers.utcnow()
    later = now + timedelta(seconds=5)

    obj1 = factory.metadata_time.create_or_read(value=now, db=db)
    obj2 = factory.metadata_time.create_or_read(value=later, db=db)

    result = crud.metadata_time.update(uuid=obj2.uuid, model=MetadataTimeUpdate(value=obj1.value), db=db)
    assert result is False
