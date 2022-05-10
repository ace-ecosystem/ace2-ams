from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.event_source import EventSourceCreate
from db import crud
from db.schemas.event_source import EventSource


def create(model: EventSourceCreate, db: Session) -> EventSource:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = EventSource(
            description=model.description,
            queues=[crud.queue.read_by_value(value=q, db=db) for q in model.queues],
            value=model.value,
        )
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> EventSource:
    return crud.helpers.read_by_uuid(db_table=EventSource, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[EventSource]:
    return crud.helpers.read_by_value(db_table=EventSource, value=value, db=db)
