from db import crud
from tests import factory


def test_delete(db):
    obj = factory.analysis_module_type.create_or_read(value="module", db=db)
    assert crud.analysis_module_type.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    # Create an analysis module type and assign it to an analysis object
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test", value="test", parent_analysis=submission.root_analysis, db=db
    )
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", cache_seconds=90, db=db)
    factory.analysis.create_or_read(
        analysis_module_type=analysis_module_type, submission=submission, target=observable, db=db
    )

    # You should not be able to delete the analysis module type now that it is in use
    assert crud.analysis_module_type.delete(uuid=analysis_module_type.uuid, db=db) is False
