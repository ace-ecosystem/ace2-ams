from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.event_vector import EventVectorCreate
from db import crud
from db.schemas.event_vector import EventVector


def create(model: EventVectorCreate, db: Session) -> EventVector:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = EventVector(
            description=model.description,
            queues=[crud.queue.read_by_value(value=q, db=db) for q in model.queues],
            value=model.value,
        )
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> EventVector:
    return crud.helpers.read_by_uuid(db_table=EventVector, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[EventVector]:
    return crud.helpers.read_by_value(db_table=EventVector, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[EventVector]:
    return crud.helpers.read_by_values(db_table=EventVector, values=values, db=db)
