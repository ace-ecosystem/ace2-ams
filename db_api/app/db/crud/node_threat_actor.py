from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_threat_actor import NodeThreatActorCreate, NodeThreatActorUpdate
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


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=NodeThreatActor, db=db)


def read_all(db: Session) -> list[NodeThreatActor]:
    return crud.helpers.read_all(db_table=NodeThreatActor, order_by=NodeThreatActor.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> NodeThreatActor:
    return crud.helpers.read_by_uuid(db_table=NodeThreatActor, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> NodeThreatActor:
    return crud.helpers.read_by_value(db_table=NodeThreatActor, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[NodeThreatActor]:
    return crud.helpers.read_by_values(db_table=NodeThreatActor, values=values, db=db)


def update(uuid: UUID, model: NodeThreatActorUpdate, db: Session) -> bool:
    obj = read_by_uuid(uuid=uuid, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = model.dict(exclude_unset=True)

    with db.begin_nested():
        try:
            if "description" in update_data:
                obj.description = update_data["description"]

            if "queues" in update_data:
                obj.queues = crud.queue.read_by_values(values=update_data["queues"], db=db)

            if "value" in update_data:
                obj.value = update_data["value"]

            db.flush()
            return True
        except IntegrityError:
            db.rollback()

    return False
