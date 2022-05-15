from sqlalchemy.orm import Session

from api_models.observable_type import ObservableTypeCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.observable_type.create_or_read(model=ObservableTypeCreate(value=value), db=db)
