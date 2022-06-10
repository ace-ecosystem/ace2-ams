from db import crud
from tests import factory


def test_delete(db):
    obj = factory.user_role.create_or_read(value="test", db=db)
    assert crud.user_role.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    obj = factory.user_role.create_or_read(value="test", db=db)

    factory.user.create_or_read(username="test", roles=["test"], db=db)

    # You should not be able to delete it now that it is in use
    assert crud.user_role.delete(uuid=obj.uuid, db=db) is False
