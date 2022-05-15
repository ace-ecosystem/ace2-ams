from sqlalchemy.orm import Session
from uuid import UUID

from api_models.event_source import EventSourceCreate
from db import crud
from db.schemas.event_source import EventSource


def create_or_read(model: EventSourceCreate, db: Session) -> EventSource:
    obj = EventSource(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        uuid=model.uuid,
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> EventSource:
    return crud.helpers.read_by_uuid(db_table=EventSource, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> EventSource:
    return crud.helpers.read_by_value(db_table=EventSource, value=value, db=db)
