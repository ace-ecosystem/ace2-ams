from sqlalchemy.orm import Session
from typing import Optional

from api_models.node_detection_point import NodeDetectionPointCreate
from db import crud
from db.schemas.node import Node


def create_or_read(node: Node, value: str, db: Session, history_username: Optional[str] = None):
    return crud.node_detection_point.create_or_read(
        model=NodeDetectionPointCreate(history_username=history_username, node_uuid=node.uuid, value=value), db=db
    )
