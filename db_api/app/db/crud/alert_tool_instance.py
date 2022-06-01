from sqlalchemy.orm import Session
from uuid import UUID

from api_models.alert_tool_instance import AlertToolInstanceCreate
from db import crud
from db.schemas.alert_tool_instance import AlertToolInstance


def create_or_read(model: AlertToolInstanceCreate, db: Session) -> AlertToolInstance:
    obj = AlertToolInstance(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> AlertToolInstance:
    return crud.helpers.read_by_uuid(db_table=AlertToolInstance, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> AlertToolInstance:
    return crud.helpers.read_by_value(db_table=AlertToolInstance, value=value, db=db)
