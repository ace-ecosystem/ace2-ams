from sqlalchemy.orm import Session
from typing import Optional

from api_models.observable_type import ObservableTypeCreate
from db import crud
from db.schemas.observable_type import ObservableType


def create(model: ObservableTypeCreate, db: Session) -> ObservableType:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = ObservableType(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_value(value: str, db: Session) -> Optional[ObservableType]:
    return crud.helpers.read_by_value(db_table=ObservableType, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[ObservableType]:
    return crud.helpers.read_by_values(db_table=ObservableType, values=values, db=db)
