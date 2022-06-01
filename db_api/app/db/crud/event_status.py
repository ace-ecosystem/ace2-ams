from sqlalchemy.orm import Session
from uuid import UUID

from api_models.event_status import EventStatusCreate
from db import crud
from db.schemas.event_status import EventStatus


def create_or_read(model: EventStatusCreate, db: Session) -> EventStatus:
    obj = EventStatus(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        uuid=model.uuid,
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> EventStatus:
    return crud.helpers.read_by_uuid(db_table=EventStatus, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> EventStatus:
    return crud.helpers.read_by_value(db_table=EventStatus, value=value, db=db)
