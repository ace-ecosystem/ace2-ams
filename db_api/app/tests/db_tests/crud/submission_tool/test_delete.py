from db import crud
from tests import factory


def test_delete(db):
    obj = factory.submission_tool.create_or_read(value="test", db=db)
    assert crud.submission_tool.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    obj = factory.submission_tool.create_or_read(value="test", db=db)

    factory.submission.create(tool="test", db=db)

    # You should not be able to delete it now that it is in use
    assert crud.submission_tool.delete(uuid=obj.uuid, db=db) is False
