from api_models.node_detection_point import NodeDetectionPointCreate
from db import crud
from tests import factory


def test_create(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )

    obj = crud.node_detection_point.create_or_read(
        model=NodeDetectionPointCreate(
            node_uuid=observable.uuid, value="test detection point", history_username="analyst"
        ),
        db=db,
    )

    assert obj.node == observable
    assert obj.value == "test detection point"


def test_create_duplicate(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )

    obj = crud.node_detection_point.create_or_read(
        model=NodeDetectionPointCreate(node_uuid=observable.uuid, value="test detection point"),
        db=db,
    )

    obj2 = crud.node_detection_point.create_or_read(
        model=NodeDetectionPointCreate(node_uuid=observable.uuid, value="test detection point"), db=db
    )

    assert obj2.uuid == obj.uuid
