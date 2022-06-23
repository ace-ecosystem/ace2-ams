from api_models.submission_comment import SubmissionCommentCreate
from db import crud
from tests import factory


def test_create(db):
    submission = factory.submission.create(db=db)
    obj = crud.submission_comment.create_or_read(
        model=SubmissionCommentCreate(submission_uuid=submission.uuid, username="analyst", value="test"), db=db
    )

    assert obj.value == "test"


def test_create_duplicate_value(db):
    submission = factory.submission.create(db=db)
    obj1 = crud.submission_comment.create_or_read(
        model=SubmissionCommentCreate(submission_uuid=submission.uuid, username="analyst", value="test"), db=db
    )
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.submission_comment.create_or_read(
        model=SubmissionCommentCreate(submission_uuid=submission.uuid, username="analyst", value=obj1.value), db=db
    )
    assert obj2.uuid == obj1.uuid
    assert obj2.value == obj1.value
