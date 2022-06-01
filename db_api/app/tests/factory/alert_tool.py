from sqlalchemy.orm import Session

from api_models.alert_tool import AlertToolCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.alert_tool.create_or_read(model=AlertToolCreate(value=value), db=db)
