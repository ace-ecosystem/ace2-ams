from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_detection_point import NodeDetectionPointCreate
from db import crud
from db.schemas.node_detection_point import NodeDetectionPoint


def create_or_read(model: NodeDetectionPointCreate, db: Session) -> NodeDetectionPoint:
    obj = NodeDetectionPoint(node=crud.node.read_by_uuid(model.node_uuid, db=db), value=model.value)

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_node_value(node_uuid=model.node_uuid, value=model.value, db=db)


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
