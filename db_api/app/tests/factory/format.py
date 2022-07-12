from sqlalchemy.orm import Session

from api_models.format import FormatCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.format.create_or_read(model=FormatCreate(value=value), db=db)
