from sqlalchemy.orm import Session

from api_models.alert_tool_instance import AlertToolInstanceCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.alert_tool_instance.create_or_read(model=AlertToolInstanceCreate(value=value), db=db)
