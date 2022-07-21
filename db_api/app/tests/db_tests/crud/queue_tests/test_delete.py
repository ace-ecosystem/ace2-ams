from db import crud
from tests import factory


def test_delete(db):
    obj = factory.queue.create_or_read(value="test", db=db)
    assert crud.queue.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    obj = factory.queue.create_or_read(value="test", db=db)

    factory.event_prevention_tool.create_or_read(value="test", queues=["test"], db=db)

    # You should not be able to delete it now that it is in use
    assert crud.queue.delete(uuid=obj.uuid, db=db) is False
