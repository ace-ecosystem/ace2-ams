from sqlalchemy.orm import Session

from api_models.submission_comment import SubmissionCommentCreate
from db import crud
from db.schemas.submission import Submission
from tests import factory


def create_or_read(submission: Submission, username: str, value: str, db: Session):
    factory.user.create_or_read(username=username, db=db)

    obj = crud.submission_comment.create_or_read(
        model=SubmissionCommentCreate(submission_uuid=submission.uuid, username=username, value=value), db=db
    )

    db.commit()
    return obj
