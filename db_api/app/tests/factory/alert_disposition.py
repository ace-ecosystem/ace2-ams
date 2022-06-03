from sqlalchemy.orm import Session

from api_models.alert_disposition import AlertDispositionCreate
from db import crud


def create_or_read(value: str, rank: int, db: Session):
    return crud.alert_disposition.create_or_read(model=AlertDispositionCreate(value=value, rank=rank), db=db)
