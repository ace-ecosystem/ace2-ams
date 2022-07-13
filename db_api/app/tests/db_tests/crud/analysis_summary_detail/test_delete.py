from db import crud
from tests import factory


def test_delete(db):
    submission = factory.submission.create(db=db)

    obj = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", db=db
    )
    assert crud.analysis_summary_detail.delete(uuid=obj.uuid, db=db) is True
