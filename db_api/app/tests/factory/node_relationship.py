from sqlalchemy.orm import Session
from typing import Optional

from api_models.node_relationship import NodeRelationshipCreate
from db import crud
from db.schemas.node import Node
from tests import factory


def create_or_read(node: Node, related_node: Node, type: str, db: Session, history_username: Optional[str] = None):
    factory.node_relationship_type.create_or_read(value=type, db=db)

    obj = crud.node_relationship.create_or_read(
        model=NodeRelationshipCreate(
            history_username=history_username, node_uuid=node.uuid, related_node_uuid=related_node.uuid, type=type
        ),
        db=db,
    )

    db.commit()
    return obj
