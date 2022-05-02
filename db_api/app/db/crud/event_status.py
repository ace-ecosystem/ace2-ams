from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.event_status import EventStatusCreate
from db import crud
from db.schemas.event_status import EventStatus


def create(model: EventStatusCreate, db: Session) -> EventStatus:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = EventStatus(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> EventStatus:
    return crud.helpers.read_by_uuid(db_table=EventStatus, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[EventStatus]:
    return crud.helpers.read_by_value(db_table=EventStatus, value=value, db=db)
