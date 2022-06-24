from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from api_models.event_comment import EventCommentCreate, EventCommentUpdate
from db import crud
from db.schemas.event import EventHistory
from db.schemas.event_comment import EventComment


def create_or_read(model: EventCommentCreate, db: Session) -> EventComment:
    # Read the event from the database
    event = crud.event.read_by_uuid(uuid=model.event_uuid, db=db)

    obj = EventComment(
        event_uuid=event.uuid,
        user=crud.user.read_by_username(username=model.username, db=db),
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        # Adding a comment counts as modifying the event, so update its version
        event.version = uuid4()
        db.flush()

        # Add a history entry
        crud.history.record_update_history(
            history_table=EventHistory,
            action_by=obj.user,
            record=event,
            diffs=[crud.history.Diff(field="comments", added_to_list=[obj.value], removed_from_list=[])],
            db=db,
        )

        db.flush()
        return obj

    return read_by_event_value(event_uuid=model.event_uuid, value=model.value, db=db)


def delete(uuid: UUID, history_username: str, db: Session) -> bool:
    # Read the comment from the database
    comment = read_by_uuid(uuid=uuid, db=db)

    # Deleting the comment counts as modifying the event, so it should receive a new version
    comment.event.version = uuid4()

    # Delete the comment
    result = crud.helpers.delete(uuid=uuid, db_table=EventComment, db=db)

    # Add an entry to the history table for deleting the comment
    crud.history.record_update_history(
        history_table=EventHistory,
        action_by=crud.user.read_by_username(username=history_username, db=db),
        record=comment.event,
        diffs=[crud.history.Diff(field="comments", added_to_list=[], removed_from_list=[comment.value])],
        db=db,
    )

    return result


def read_by_event_value(event_uuid: UUID, value: str, db: Session) -> EventComment:
    return (
        db.execute(select(EventComment).where(EventComment.event_uuid == event_uuid, EventComment.value == value))
        .scalars()
        .one()
    )


def read_by_uuid(uuid: UUID, db: Session) -> EventComment:
    return crud.helpers.read_by_uuid(db_table=EventComment, uuid=uuid, db=db)


def update(uuid: UUID, model: EventCommentUpdate, db: Session) -> bool:
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

    # Modifying the comment counts as modifying the event, so it should receive a new version
    comment.event.version = uuid4()

    # Add an entry to the history table for updating the comment
    crud.history.record_update_history(
        history_table=EventHistory,
        record=comment.event,
        action_by=comment.user,
        diffs=[diff],
        db=db,
    )

    return True
