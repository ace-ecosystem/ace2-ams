from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.event_risk_level import EventRiskLevelCreate
from db import crud
from db.schemas.event_risk_level import EventRiskLevel


def create(model: EventRiskLevelCreate, db: Session) -> EventRiskLevel:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = EventRiskLevel(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> EventRiskLevel:
    return crud.helpers.read_by_uuid(db_table=EventRiskLevel, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[EventRiskLevel]:
    return crud.helpers.read_by_value(db_table=EventRiskLevel, value=value, db=db)
