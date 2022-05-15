from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_threat_actor import NodeThreatActorCreate
from db import crud
from db.schemas.node_threat_actor import NodeThreatActor


def create_or_read(model: NodeThreatActorCreate, db: Session) -> NodeThreatActor:
    obj = NodeThreatActor(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        uuid=model.uuid,
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> NodeThreatActor:
    return crud.helpers.read_by_uuid(db_table=NodeThreatActor, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> NodeThreatActor:
    return crud.helpers.read_by_value(db_table=NodeThreatActor, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[NodeThreatActor]:
    return crud.helpers.read_by_values(db_table=NodeThreatActor, values=values, db=db)
