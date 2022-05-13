from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_threat_type import NodeThreatTypeCreate
from db import crud
from db.schemas.node_threat_type import NodeThreatType


def create_or_read(model: NodeThreatTypeCreate, db: Session) -> NodeThreatType:
    obj = NodeThreatType(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> NodeThreatType:
    return crud.helpers.read_by_uuid(db_table=NodeThreatType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> NodeThreatType:
    return crud.helpers.read_by_value(db_table=NodeThreatType, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[NodeThreatType]:
    return crud.helpers.read_by_values(db_table=NodeThreatType, values=values, db=db)
