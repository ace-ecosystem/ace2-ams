from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_comment import NodeCommentCreate, NodeCommentUpdate
from db import crud
from db.schemas.node_comment import NodeComment


def create_or_read(model: NodeCommentCreate, db: Session) -> NodeComment:
    node = crud.node.read_by_uuid(uuid=model.node_uuid, db=db)

    obj = NodeComment(
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
    result = crud.helpers.delete(uuid=uuid, db_table=NodeComment, db=db)

    # Add an entry to the appropriate node history table for deleting the comment
    crud.history.record_node_update_history(
        record_node=comment.node,
        action_by=crud.user.read_by_username(username=history_username, db=db),
        diffs=[crud.history.Diff(field="comments", added_to_list=[], removed_from_list=[comment.value])],
        db=db,
    )

    return result


def read_by_node_value(node_uuid: UUID, value: str, db: Session) -> NodeComment:
    return (
        db.execute(select(NodeComment).where(NodeComment.node_uuid == node_uuid, NodeComment.value == value))
        .scalars()
        .one()
    )


def read_by_uuid(uuid: UUID, db: Session) -> NodeComment:
    return crud.helpers.read_by_uuid(db_table=NodeComment, uuid=uuid, db=db)


def update(uuid: UUID, model: NodeCommentUpdate, db: Session):
    # Read the comment from the database
    comment = read_by_uuid(uuid=uuid, db=db)

    # Update the user and timestamp on the comment
    comment.user = crud.user.read_by_username(username=model.username, db=db)
    comment.insert_time = crud.helpers.utcnow()

    # Set the new comment value
    diff = crud.history.Diff(field="comments", added_to_list=[model.value], removed_from_list=[comment.value])
    comment.value = model.value

    # Modifying the comment counts as modifying the Node, so it should receive a new version
    crud.node.update_version(node=comment.node, db=db)

    # Add an entry to the appropriate node history table for updating the comment
    crud.history.record_node_update_history(
        record_node=comment.node,
        action_by=comment.user,
        diffs=[diff],
        db=db,
    )
