from api_models.analysis_summary_detail import AnalysisSummaryDetailCreate
from db import crud
from tests import factory


def test_create(db):
    submission = factory.submission.create(db=db)
    factory.format.create_or_read(value="PRE", db=db)

    obj = crud.analysis_summary_detail.create_or_read(
        model=AnalysisSummaryDetailCreate(
            analysis_uuid=submission.root_analysis_uuid,
            content="test",
            format="PRE",
            header="test",
        ),
        db=db,
    )

    assert obj.analysis_uuid == submission.root_analysis_uuid
    assert obj.content == "test"
    assert obj.format.value == "PRE"
    assert obj.header == "test"


def test_create_duplicate_value(db):
    submission = factory.submission.create(db=db)
    factory.format.create_or_read(value="PRE", db=db)

    obj1 = crud.analysis_summary_detail.create_or_read(
        model=AnalysisSummaryDetailCreate(
            analysis_uuid=submission.root_analysis_uuid,
            content="test",
            format="PRE",
            header="test",
        ),
        db=db,
    )
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.analysis_summary_detail.create_or_read(
        model=AnalysisSummaryDetailCreate(
            analysis_uuid=submission.root_analysis_uuid,
            content=obj1.content,
            format="PRE",
            header=obj1.header,
        ),
        db=db,
    )
    assert obj2.uuid == obj1.uuid
