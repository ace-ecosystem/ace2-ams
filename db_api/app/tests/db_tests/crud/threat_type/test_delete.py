from db import crud
from tests import factory


def test_delete(db):
    obj = factory.threat_type.create_or_read(value="test", db=db)
    assert crud.threat_type.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    obj = factory.threat_type.create_or_read(value="test", db=db)
    factory.threat.create_or_read(value="test", types=["test"], db=db)

    # You should not be able to delete it now that it is in use
    assert crud.threat_type.delete(uuid=obj.uuid, db=db) is False
