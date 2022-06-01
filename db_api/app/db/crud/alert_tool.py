from sqlalchemy.orm import Session
from uuid import UUID

from api_models.alert_tool import AlertToolCreate
from db import crud
from db.schemas.alert_tool import AlertTool


def create_or_read(model: AlertToolCreate, db: Session) -> AlertTool:
    obj = AlertTool(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> AlertTool:
    return crud.helpers.read_by_uuid(db_table=AlertTool, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> AlertTool:
    return crud.helpers.read_by_value(db_table=AlertTool, value=value, db=db)
