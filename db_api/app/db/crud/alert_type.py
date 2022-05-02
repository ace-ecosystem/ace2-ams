from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.alert_type import AlertTypeCreate
from db import crud
from db.schemas.alert_type import AlertType


def create(model: AlertTypeCreate, db: Session) -> AlertType:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = AlertType(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> AlertType:
    return crud.helpers.read_by_uuid(db_table=AlertType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[AlertType]:
    return crud.helpers.read_by_value(db_table=AlertType, value=value, db=db)
