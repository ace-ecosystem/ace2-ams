from api_models.analysis_summary_detail import AnalysisSummaryDetailUpdate
from db import crud
from tests import factory


def test_update(db):
    submission = factory.submission.create(db=db)
    factory.format.create_or_read(value="PRE", db=db)
    factory.format.create_or_read(value="TEXT", db=db)

    obj = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", format="PRE", db=db
    )

    assert obj.content == "test"
    assert obj.header == "test"
    assert obj.format.value == "PRE"

    crud.analysis_summary_detail.update(
        uuid=obj.uuid,
        model=AnalysisSummaryDetailUpdate(content="new content", header="new header", format="TEXT"),
        db=db,
    )

    assert obj.content == "new content"
    assert obj.header == "new header"
    assert obj.format.value == "TEXT"


def test_update_duplicate(db):
    submission = factory.submission.create(db=db)

    obj1 = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, content="test1", header="test1", db=db
    )
    obj2 = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, content="test2", header="test2", db=db
    )

    result = crud.analysis_summary_detail.update(
        uuid=obj2.uuid, model=AnalysisSummaryDetailUpdate(content="test1", header="test1"), db=db
    )
    assert result is False
