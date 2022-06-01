from sqlalchemy.orm import Session
from uuid import UUID

from api_models.alert_type import AlertTypeCreate
from db import crud
from db.schemas.alert_type import AlertType


def create_or_read(model: AlertTypeCreate, db: Session) -> AlertType:
    obj = AlertType(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> AlertType:
    return crud.helpers.read_by_uuid(db_table=AlertType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> AlertType:
    return crud.helpers.read_by_value(db_table=AlertType, value=value, db=db)
