from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_threat import NodeThreatCreate
from db import crud
from db.schemas.node_threat import NodeThreat


def create_or_read(model: NodeThreatCreate, db: Session) -> NodeThreat:
    obj = NodeThreat(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        types=crud.node_threat_type.read_by_values(values=model.types, db=db),
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> NodeThreat:
    return crud.helpers.read_by_uuid(db_table=NodeThreat, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> NodeThreat:
    return crud.helpers.read_by_value(db_table=NodeThreat, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[NodeThreat]:
    return crud.helpers.read_by_values(db_table=NodeThreat, values=values, db=db)
