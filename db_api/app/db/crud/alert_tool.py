from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.alert_tool import AlertToolCreate
from db import crud
from db.schemas.alert_tool import AlertTool


def create(model: AlertToolCreate, db: Session) -> AlertTool:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = AlertTool(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> AlertTool:
    return crud.helpers.read_by_uuid(db_table=AlertTool, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[AlertTool]:
    return crud.helpers.read_by_value(db_table=AlertTool, value=value, db=db)
