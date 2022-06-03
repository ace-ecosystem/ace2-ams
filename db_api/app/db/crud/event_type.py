from sqlalchemy.orm import Session
from uuid import UUID

from api_models.event_type import EventTypeCreate
from db import crud
from db.schemas.event_type import EventType


def create_or_read(model: EventTypeCreate, db: Session) -> EventType:
    obj = EventType(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        uuid=model.uuid,
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> EventType:
    return crud.helpers.read_by_uuid(db_table=EventType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> EventType:
    return crud.helpers.read_by_value(db_table=EventType, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[EventType]:
    return crud.helpers.read_by_values(db_table=EventType, values=values, db=db)
