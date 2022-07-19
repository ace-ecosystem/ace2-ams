from db import crud
from tests import factory


def test_delete(db):
    obj = factory.format.create_or_read(value="test", db=db)
    assert crud.format.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    obj = factory.format.create_or_read(value="PRE", db=db)

    submission = factory.submission.create(db=db)
    factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", format="PRE", db=db
    )

    # You should not be able to delete it now that it is in use
    assert crud.format.delete(uuid=obj.uuid, db=db) is False
