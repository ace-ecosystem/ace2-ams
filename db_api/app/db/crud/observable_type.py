from sqlalchemy.orm import Session
from uuid import UUID

from api_models.observable_type import ObservableTypeCreate, ObservableTypeUpdate
from db import crud
from db.schemas.observable_type import ObservableType


def create_or_read(model: ObservableTypeCreate, db: Session) -> ObservableType:
    obj = ObservableType(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=ObservableType, db=db)


def read_all(db: Session) -> list[ObservableType]:
    return crud.helpers.read_all(db_table=ObservableType, order_by=ObservableType.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> ObservableType:
    return crud.helpers.read_by_uuid(db_table=ObservableType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> ObservableType:
    return crud.helpers.read_by_value(db_table=ObservableType, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[ObservableType]:
    return crud.helpers.read_by_values(db_table=ObservableType, values=values, db=db)


def update(uuid: UUID, model: ObservableTypeUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=ObservableType, db=db)
