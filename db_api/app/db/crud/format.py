from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.format import FormatCreate, FormatUpdate
from db import crud
from db.schemas.format import Format


def build_read_all_query() -> Select:
    return select(Format).order_by(Format.value)


def create_or_read(model: FormatCreate, db: Session) -> Format:
    obj = Format(description=model.description, uuid=model.uuid, value=model.value)

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=Format, db=db)


def read_all(db: Session) -> list[Format]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> Format:
    return crud.helpers.read_by_uuid(db_table=Format, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Format:
    return crud.helpers.read_by_value(db_table=Format, value=value, db=db)


def update(uuid: UUID, model: FormatUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=Format, db=db)
