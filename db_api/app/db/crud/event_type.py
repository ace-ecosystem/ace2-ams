from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.event_type import EventTypeCreate
from db import crud
from db.schemas.event_type import EventType


def create(model: EventTypeCreate, db: Session) -> EventType:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = EventType(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> EventType:
    return crud.helpers.read_by_uuid(db_table=EventType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[EventType]:
    return crud.helpers.read_by_value(db_table=EventType, value=value, db=db)
