from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.event_vector import EventVectorCreate
from db import crud
from db.schemas.event_vector import EventVector


def create(model: EventVectorCreate, db: Session) -> EventVector:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = EventVector(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> EventVector:
    return crud.helpers.read_by_uuid(db_table=EventVector, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[EventVector]:
    return crud.helpers.read_by_value(db_table=EventVector, value=value, db=db)
