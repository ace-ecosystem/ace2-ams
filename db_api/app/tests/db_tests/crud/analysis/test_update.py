import json

from api_models.analysis import AnalysisUpdate
from db import crud
from tests import factory


def test_update(db):
    factory.analysis_status.create_or_read(value="running", db=db)
    factory.analysis_status.create_or_read(value="complete", db=db)

    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test", value="test", parent_analysis=submission.root_analysis, db=db
    )
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", cache_seconds=90, db=db)

    analysis = factory.analysis.create_or_read(
        analysis_module_type=analysis_module_type, status="running", submission=submission, target=observable, db=db
    )

    assert analysis.details is None
    assert analysis.error_message is None
    assert analysis.stack_trace is None

    crud.analysis.update(
        uuid=analysis.uuid,
        model=AnalysisUpdate(
            details=json.dumps({"foo": "bar"}),
            error_message="test error",
            stack_trace="test stack trace",
            status="complete",
        ),
        db=db,
    )

    assert analysis.details == {"foo": "bar"}
    assert analysis.error_message == "test error"
    assert analysis.stack_trace == "test stack trace"
    assert analysis.status.value == "complete"
