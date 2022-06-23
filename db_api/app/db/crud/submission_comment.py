from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from api_models.submission_comment import SubmissionCommentCreate, SubmissionCommentUpdate
from db import crud
from db.schemas.submission import SubmissionHistory
from db.schemas.submission_comment import SubmissionComment


def create_or_read(model: SubmissionCommentCreate, db: Session) -> SubmissionComment:
    # Read the submission from the database
    submission = crud.submission.read_by_uuid(uuid=model.submission_uuid, db=db)

    obj = SubmissionComment(
        submission_uuid=submission.uuid,
        user=crud.user.read_by_username(username=model.username, db=db),
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        # Adding a comment counts as modifying the submission, so update its version
        submission.version = uuid4()

        # Add a history entry
        crud.history.record_update_history(
            history_table=SubmissionHistory,
            action_by=obj.user,
            record=submission,
            diffs=[crud.history.Diff(field="comments", added_to_list=[obj.value], removed_from_list=[])],
            db=db,
        )

        db.flush()
        return obj

    return read_by_submission_value(submission_uuid=model.submission_uuid, value=model.value, db=db)


def delete(uuid: UUID, history_username: str, db: Session) -> bool:
    # Read the comment from the database
    comment = read_by_uuid(uuid=uuid, db=db)

    # Deleting the comment counts as modifying the submission, so it should receive a new version
    comment.submission.version = uuid4()

    # Delete the comment
    result = crud.helpers.delete(uuid=uuid, db_table=SubmissionComment, db=db)

    # Add an entry to the history table for deleting the comment
    crud.history.record_update_history(
        history_table=SubmissionHistory,
        action_by=crud.user.read_by_username(username=history_username, db=db),
        record=comment.submission,
        diffs=[crud.history.Diff(field="comments", added_to_list=[], removed_from_list=[comment.value])],
        db=db,
    )

    return result


def read_by_submission_value(submission_uuid: UUID, value: str, db: Session) -> SubmissionComment:
    return (
        db.execute(
            select(SubmissionComment).where(
                SubmissionComment.submission_uuid == submission_uuid, SubmissionComment.value == value
            )
        )
        .scalars()
        .one()
    )


def read_by_uuid(uuid: UUID, db: Session) -> SubmissionComment:
    return crud.helpers.read_by_uuid(db_table=SubmissionComment, uuid=uuid, db=db)


def update(uuid: UUID, model: SubmissionCommentUpdate, db: Session) -> bool:
    with db.begin_nested():
        # Read the comment from the database
        comment = read_by_uuid(uuid=uuid, db=db)

        # Update the user and timestamp on the comment
        comment.user = crud.user.read_by_username(username=model.username, db=db)
        comment.insert_time = crud.helpers.utcnow()

        # Set the new comment value
        diff = crud.history.Diff(field="comments", added_to_list=[model.value], removed_from_list=[comment.value])
        comment.value = model.value

        # Try to flush the changes to the database
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            return False

    # Modifying the comment counts as modifying the submission, so it should receive a new version
    comment.submission.version = uuid4()

    # Add an entry to the appropriate node history table for updating the comment
    crud.history.record_update_history(
        history_table=SubmissionHistory,
        record=comment.submission,
        action_by=comment.user,
        diffs=[diff],
        db=db,
    )

    return True
