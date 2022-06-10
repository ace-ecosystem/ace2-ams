from api_models.user_role import UserRoleUpdate
from db import crud
from tests import factory


def test_update(db):
    obj = factory.user_role.create_or_read(value="test", db=db)

    assert obj.description is None
    assert obj.value == "test"

    crud.user_role.update(
        uuid=obj.uuid,
        model=UserRoleUpdate(description="test description", value="new value"),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.value == "new value"


def test_update_duplicate_value(db):
    obj1 = factory.user_role.create_or_read(value="test", db=db)
    obj2 = factory.user_role.create_or_read(value="test2", db=db)

    result = crud.user_role.update(uuid=obj2.uuid, model=UserRoleUpdate(value=obj1.value), db=db)
    assert result is False
