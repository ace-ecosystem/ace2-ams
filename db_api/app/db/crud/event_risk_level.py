from sqlalchemy.orm import Session
from uuid import UUID

from api_models.event_risk_level import EventRiskLevelCreate
from db import crud
from db.schemas.event_risk_level import EventRiskLevel


def create_or_read(model: EventRiskLevelCreate, db: Session) -> EventRiskLevel:
    obj = EventRiskLevel(
        description=model.description,
        queues=crud.queue.read_by_values(values=model.queues, db=db),
        uuid=model.uuid,
        value=model.value,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> EventRiskLevel:
    return crud.helpers.read_by_uuid(db_table=EventRiskLevel, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> EventRiskLevel:
    return crud.helpers.read_by_value(db_table=EventRiskLevel, value=value, db=db)
