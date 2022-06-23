from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.event_comment import EventCommentCreate, EventCommentUpdate
from db import crud
from db_api.app.db.schemas.event_comment import EventComment


def create_or_read(model: EventCommentCreate, db: Session) -> EventComment:
    node = crud.node.read_by_uuid(uuid=model.node_uuid, db=db)

    obj = EventComment(
        node=node,
        user=crud.user.read_by_username(username=model.username, db=db),
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        # Adding a comment counts as modifying the Node, so update its version
        crud.node.update_version(node=node, db=db)

        # Add a history entry
        crud.history.record_node_update_history(
            record_node=node,
            action_by=obj.user,
            diffs=[crud.history.Diff(field="comments", added_to_list=[obj.value], removed_from_list=[])],
            db=db,
        )

        db.flush()
        return obj

    return read_by_node_value(node_uuid=model.node_uuid, value=model.value, db=db)


def delete(uuid: UUID, history_username: str, db: Session) -> bool:
    # Read the comment from the database
    comment = read_by_uuid(uuid=uuid, db=db)

    # Deleting the comment counts as modifying the Node, so it should receive a new version
    crud.node.update_version(node=comment.node, db=db)

    # Delete the comment
    result = crud.helpers.delete(uuid=uuid, db_table=EventComment, db=db)

    # Add an entry to the appropriate node history table for deleting the comment
    crud.history.record_node_update_history(
        record_node=comment.node,
        action_by=crud.user.read_by_username(username=history_username, db=db),
        diffs=[crud.history.Diff(field="comments", added_to_list=[], removed_from_list=[comment.value])],
        db=db,
    )

    return result


def read_by_node_value(node_uuid: UUID, value: str, db: Session) -> EventComment:
    return (
        db.execute(select(EventComment).where(EventComment.node_uuid == node_uuid, EventComment.value == value))
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

    # Modifying the comment counts as modifying the Node, so it should receive a new version
    crud.node.update_version(node=comment.node, db=db)

    # Add an entry to the appropriate node history table for updating the comment
    crud.history.record_node_update_history(
        record_node=comment.node,
        action_by=comment.user,
        diffs=[diff],
        db=db,
    )

    return True
