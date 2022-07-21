from db import crud
from tests import factory


def test_delete(db):
    submission = factory.submission.create(db=db)
    obj = factory.submission_comment.create_or_read(submission=submission, username="analyst", value="test", db=db)
    assert crud.submission_comment.delete(uuid=obj.uuid, history_username="analyst", db=db) is True
