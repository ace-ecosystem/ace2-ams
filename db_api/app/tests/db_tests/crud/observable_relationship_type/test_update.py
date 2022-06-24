from api_models.observable_relationship_type import ObservableRelationshipTypeUpdate
from db import crud
from tests import factory


def test_update(db):
    obj = factory.observable_relationship_type.create_or_read(value="test", db=db)

    assert obj.description is None
    assert obj.value == "test"

    crud.observable_relationship_type.update(
        uuid=obj.uuid,
        model=ObservableRelationshipTypeUpdate(description="test description", value="new value"),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.value == "new value"


def test_update_duplicate_value(db):
    obj1 = factory.observable_relationship_type.create_or_read(value="test", db=db)
    obj2 = factory.observable_relationship_type.create_or_read(value="test2", db=db)

    result = crud.observable_relationship_type.update(
        uuid=obj2.uuid, model=ObservableRelationshipTypeUpdate(value=obj1.value), db=db
    )
    assert result is False
