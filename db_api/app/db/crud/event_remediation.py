from sqlalchemy.orm import Session
from uuid import UUID

from api_models.event_remediation import EventRemediationCreate
from db import crud
from db.schemas.event_remediation import EventRemediation


def create_or_read(model: EventRemediationCreate, db: Session) -> EventRemediation:
    obj = EventRemediation(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        uuid=model.uuid,
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> EventRemediation:
    return crud.helpers.read_by_uuid(db_table=EventRemediation, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> EventRemediation:
    return crud.helpers.read_by_value(db_table=EventRemediation, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[EventRemediation]:
    return crud.helpers.read_by_values(db_table=EventRemediation, values=values, db=db)
