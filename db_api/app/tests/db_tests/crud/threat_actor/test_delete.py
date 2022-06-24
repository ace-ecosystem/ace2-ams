from db import crud
from tests import factory


def test_delete(db):
    obj = factory.threat_actor.create_or_read(value="test", db=db)
    assert crud.threat_actor.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    obj = factory.threat_actor.create_or_read(value="test", db=db)
    factory.event.create_or_read(name="test", threat_actors=["test"], db=db)

    # You should not be able to delete it now that it is in use
    assert crud.threat_actor.delete(uuid=obj.uuid, db=db) is False
