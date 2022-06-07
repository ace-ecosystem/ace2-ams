from api_models.node_detection_point import NodeDetectionPointUpdate
from db import crud
from tests import factory


def test_update(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )
    obj = factory.node_detection_point.create_or_read(node=observable, value="test detection point", db=db)
    initial_insert_time = obj.insert_time

    assert obj.node == observable
    assert obj.value == "test detection point"

    result = crud.node_detection_point.update(
        uuid=obj.uuid,
        model=NodeDetectionPointUpdate(history_username="analyst", value="new value"),
        db=db,
    )

    assert result is True
    assert obj.insert_time != initial_insert_time
    assert obj.node == observable
    assert obj.value == "new value"


def test_update_conflicting_value(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )
    obj = factory.node_detection_point.create_or_read(node=observable, value="test detection point", db=db)
    obj2 = factory.node_detection_point.create_or_read(node=observable, value="test detection point 2", db=db)

    result = crud.node_detection_point.update(
        uuid=obj2.uuid,
        model=NodeDetectionPointUpdate(history_username="analyst", value=obj.value),
        db=db,
    )

    assert result is False
    assert obj2.value == "test detection point 2"
