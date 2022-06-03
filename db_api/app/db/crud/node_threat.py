from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_threat import NodeThreatCreate, NodeThreatUpdate
from db import crud
from db.schemas.node_threat import NodeThreat


def create_or_read(model: NodeThreatCreate, db: Session) -> NodeThreat:
    obj = NodeThreat(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        types=crud.node_threat_type.read_by_values(values=model.types, db=db),
        uuid=model.uuid,
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


def update(uuid: UUID, model: NodeThreatUpdate, db: Session) -> bool:
    with db.begin_nested():
        obj = read_by_uuid(uuid=uuid, db=db)

        # Get the data that was given in the request and use it to update the database object
        update_data = model.dict(exclude_unset=True)

        if "description" in update_data:
            obj.description = update_data["description"]

        if "queues" in update_data:
            obj.queues = crud.queue.read_by_values(values=update_data["queues"], db=db)

        if "value" in update_data:
            obj.value = update_data["value"]

        if "types" in update_data:
            obj.types = crud.node_threat_type.read_by_values(values=update_data["types"], db=db)

        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            return False

    return True
