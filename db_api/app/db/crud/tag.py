from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.tag import TagCreate, TagUpdate
from db import crud
from db.schemas.tag import Tag


def build_read_all_query() -> Select:
    return select(Tag).order_by(Tag.value)


def create_or_read(model: TagCreate, db: Session) -> Tag:
    obj = Tag(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=Tag, db=db)


def read_all(db: Session) -> list[Tag]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> Tag:
    return crud.helpers.read_by_uuid(db_table=Tag, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Tag:
    return crud.helpers.read_by_value(db_table=Tag, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[Tag]:
    return crud.helpers.read_by_values(db_table=Tag, values=values, db=db)


def update(uuid: UUID, model: TagUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=Tag, db=db)
