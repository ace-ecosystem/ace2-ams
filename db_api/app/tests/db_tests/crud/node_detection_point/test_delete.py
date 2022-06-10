from db import crud
from tests import factory


def test_delete(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )
    obj = factory.node_detection_point.create_or_read(node=observable, value="test detection point", db=db)

    result = crud.node_detection_point.delete(uuid=obj.uuid, history_username="analyst", db=db)
    assert result is True
