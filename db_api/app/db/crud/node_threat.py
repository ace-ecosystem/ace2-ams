from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.node_threat import NodeThreatCreate
from db import crud
from db.schemas.node_threat import NodeThreat


def create(model: NodeThreatCreate, db: Session) -> NodeThreat:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = NodeThreat(
            description=model.description,
            queues=[crud.queue.read_by_value(value=q, db=db) for q in model.queues],
            types=[crud.node_threat_type.read_by_value(value=t, db=db) for t in model.types],
            value=model.value,
        )
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> NodeThreat:
    return crud.helpers.read_by_uuid(db_table=NodeThreat, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[NodeThreat]:
    return crud.helpers.read_by_value(db_table=NodeThreat, value=value, db=db)
