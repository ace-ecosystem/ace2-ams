from sqlalchemy.orm import Session

from api_models.observable_type import ObservableTypeCreate
from db import crud
from db.schemas.observable_type import ObservableType


def create_or_read(model: ObservableTypeCreate, db: Session) -> ObservableType:
    obj = ObservableType(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_value(value: str, db: Session) -> ObservableType:
    return crud.helpers.read_by_value(db_table=ObservableType, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[ObservableType]:
    return crud.helpers.read_by_values(db_table=ObservableType, values=values, db=db)
