from db import crud
from tests import factory


def test_delete(db):
    obj = factory.analysis_status.create_or_read(value="test", db=db)
    assert crud.analysis_status.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    obj = factory.analysis_status.create_or_read(value="test", db=db)

    submission = factory.submission.create(db=db)
    obs = factory.observable.create_or_read(type="test", value="value", parent_analysis=submission.root_analysis, db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test module", db=db)
    factory.analysis.create_or_read(
        analysis_module_type=analysis_module_type, submission=submission, target=obs, status="test", db=db
    )

    # You should not be able to delete it now that it is in use
    assert crud.analysis_status.delete(uuid=obj.uuid, db=db) is False
