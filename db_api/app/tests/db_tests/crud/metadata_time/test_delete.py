from db import crud
from tests import factory


def test_delete(db):
    obj = factory.metadata_time.create_or_read(value=crud.helpers.utcnow(), db=db)
    assert crud.metadata_time.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    now = crud.helpers.utcnow()
    obj = factory.metadata_time.create_or_read(value=now, db=db)

    submission = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, time=now, db=db
    )

    # You should not be able to delete it now that it is in use
    assert crud.metadata_time.delete(uuid=obj.uuid, db=db) is False
