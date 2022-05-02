from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.alert_tool_instance import AlertToolInstanceCreate
from db import crud
from db.schemas.alert_tool_instance import AlertToolInstance


def create(model: AlertToolInstanceCreate, db: Session) -> AlertToolInstance:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = AlertToolInstance(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> AlertToolInstance:
    return crud.helpers.read_by_uuid(db_table=AlertToolInstance, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[AlertToolInstance]:
    return crud.helpers.read_by_value(db_table=AlertToolInstance, value=value, db=db)
