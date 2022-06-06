from db import crud
from tests import factory


def test_read_all(db):
    obj1 = factory.user_role.create_or_read(value="test", db=db)
    obj2 = factory.user_role.create_or_read(value="test2", db=db)

    result = crud.user_role.read_all(db=db)
    # There is a default "test_role", so that will be the third element
    assert len(result) == 3
    assert result[0].uuid == obj1.uuid
    assert result[1].uuid == obj2.uuid
    assert result[2].value == "test_role"


def test_read_by_uuid(db):
    obj = factory.user_role.create_or_read(value="test", db=db)

    result = crud.user_role.read_by_uuid(uuid=obj.uuid, db=db)
    assert result.uuid == obj.uuid


def test_read_by_value(db):
    obj = factory.user_role.create_or_read(value="test", db=db)

    result = crud.user_role.read_by_value(value=obj.value, db=db)
    assert result.uuid == obj.uuid
