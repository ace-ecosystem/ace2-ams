from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_detection_point import NodeDetectionPointCreate, NodeDetectionPointUpdate
from db import crud
from db.schemas.node_detection_point import NodeDetectionPoint


def create_or_read(model: NodeDetectionPointCreate, db: Session) -> NodeDetectionPoint:
    obj = NodeDetectionPoint(node=crud.node.read_by_uuid(model.node_uuid, db=db), value=model.value)

    if crud.helpers.create(obj=obj, db=db):
        # Adding a detection point counts as modifying the Node, so update its version
        crud.node.update_version(node=obj.node, db=db)

        # Add a history entry
        if model.history_username:
            crud.history.record_node_update_history(
                record_node=obj.node,
                action_by=crud.user.read_by_username(username=model.history_username, db=db),
                diffs=[crud.history.Diff(field="detection_points", added_to_list=[obj.value], removed_from_list=[])],
                db=db,
            )

        db.flush()
        return obj

    return read_by_node_value(node_uuid=model.node_uuid, value=model.value, db=db)


def delete(uuid: UUID, history_username: str, db: Session) -> bool:
    # Read detection point from the database
    detection_point = read_by_uuid(uuid=uuid, db=db)

    # Deleting the detection point counts as modifying the Node, so it should receive a new version
    crud.node.update_version(node=detection_point.node, db=db)

    # Delete the detection point
    result = crud.helpers.delete(uuid=uuid, db_table=NodeDetectionPoint, db=db)

    # Add an entry to the appropriate node history table for deleting the detection point
    crud.history.record_node_update_history(
        record_node=detection_point.node,
        action_by=crud.user.read_by_username(username=history_username, db=db),
        diffs=[
            crud.history.Diff(field="detection_points", added_to_list=[], removed_from_list=[detection_point.value])
        ],
        db=db,
    )

    return result


def read_by_node_value(node_uuid: UUID, value: str, db: Session) -> NodeDetectionPoint:
    return (
        db.execute(
            select(NodeDetectionPoint).where(
                NodeDetectionPoint.node_uuid == node_uuid, NodeDetectionPoint.value == value
            )
        )
        .scalars()
        .one()
    )


def read_by_uuid(uuid: UUID, db: Session) -> NodeDetectionPoint:
    return crud.helpers.read_by_uuid(db_table=NodeDetectionPoint, uuid=uuid, db=db)


def update(uuid: UUID, model: NodeDetectionPointUpdate, db: Session) -> bool:
    with db.begin_nested():
        # Read detection point from the database
        detection_point = read_by_uuid(uuid=uuid, db=db)

        # Update the timestamp on the detection point
        detection_point.insert_time = crud.helpers.utcnow()

        # Set the new detection point value
        diff = crud.history.Diff(
            field="detection_points", added_to_list=[model.value], removed_from_list=[detection_point.value]
        )
        detection_point.value = model.value

        # Try to flush the changes to the database
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            return False

    # Modifying the detection point counts as modifying the Node, so it should receive a new version
    crud.node.update_version(node=detection_point.node, db=db)

    # Add an entry to the appropriate node history table for updating the detection point
    if model.history_username:
        crud.history.record_node_update_history(
            record_node=detection_point.node,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            diffs=[diff],
            db=db,
        )

    return True
