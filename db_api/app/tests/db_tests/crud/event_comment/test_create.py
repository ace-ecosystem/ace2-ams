from api_models.event_comment import EventCommentCreate
from db import crud
from tests import factory


def test_create(db):
    event = factory.event.create_or_read(name="test", db=db)
    obj = crud.event_comment.create_or_read(
        model=EventCommentCreate(node_uuid=event.uuid, username="analyst", value="test"), db=db
    )

    assert obj.value == "test"


def test_create_duplicate_value(db):
    event = factory.event.create_or_read(name="test", db=db)
    obj1 = crud.event_comment.create_or_read(
        model=EventCommentCreate(node_uuid=event.uuid, username="analyst", value="test"), db=db
    )
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.event_comment.create_or_read(
        model=EventCommentCreate(node_uuid=event.uuid, username="analyst", value=obj1.value), db=db
    )
    assert obj2.uuid == obj1.uuid
    assert obj2.value == obj1.value
