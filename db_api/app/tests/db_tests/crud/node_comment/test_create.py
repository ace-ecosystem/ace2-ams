from api_models.node_comment import NodeCommentCreate
from db import crud
from tests import factory


def test_create(db):
    submission = factory.submission.create(db=db)
    obj = crud.node_comment.create_or_read(
        model=NodeCommentCreate(node_uuid=submission.uuid, username="analyst", value="test"), db=db
    )

    assert obj.value == "test"


def test_create_duplicate_value(db):
    submission = factory.submission.create(db=db)
    obj1 = crud.node_comment.create_or_read(
        model=NodeCommentCreate(node_uuid=submission.uuid, username="analyst", value="test"), db=db
    )
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.node_comment.create_or_read(
        model=NodeCommentCreate(node_uuid=submission.uuid, username="analyst", value=obj1.value), db=db
    )
    assert obj2.uuid == obj1.uuid
    assert obj2.value == obj1.value
