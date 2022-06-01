from sqlalchemy.orm import Session

from api_models.alert_type import AlertTypeCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.alert_type.create_or_read(model=AlertTypeCreate(value=value), db=db)
