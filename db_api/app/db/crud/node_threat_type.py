from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.node_threat_type import NodeThreatTypeCreate
from db import crud
from db.schemas.node_threat_type import NodeThreatType


def create(model: NodeThreatTypeCreate, db: Session) -> NodeThreatType:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = NodeThreatType(
            description=model.description,
            queues=[crud.queue.read_by_value(value=q, db=db) for q in model.queues],
            value=model.value,
        )
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> NodeThreatType:
    return crud.helpers.read_by_uuid(db_table=NodeThreatType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[NodeThreatType]:
    return crud.helpers.read_by_value(db_table=NodeThreatType, value=value, db=db)
