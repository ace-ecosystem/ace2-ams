from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.alert_disposition import AlertDispositionCreate
from db import crud
from db.schemas.alert_disposition import AlertDisposition


def create(model: AlertDispositionCreate, db: Session) -> AlertDisposition:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = AlertDisposition(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> AlertDisposition:
    return crud.helpers.read_by_uuid(db_table=AlertDisposition, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[AlertDisposition]:
    return crud.helpers.read_by_value(db_table=AlertDisposition, value=value, db=db)
