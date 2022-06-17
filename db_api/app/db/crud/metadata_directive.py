from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.metadata_directive import MetadataDirectiveCreate, MetadataDirectiveUpdate
from db import crud
from db.schemas.metadata_directive import MetadataDirective


def build_read_all_query() -> Select:
    return select(MetadataDirective).order_by(MetadataDirective.value)


def create_or_read(model: MetadataDirectiveCreate, db: Session) -> MetadataDirective:
    obj = MetadataDirective(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=MetadataDirective, db=db)


def read_all(db: Session) -> list[MetadataDirective]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> MetadataDirective:
    return crud.helpers.read_by_uuid(db_table=MetadataDirective, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> MetadataDirective:
    return crud.helpers.read_by_value(db_table=MetadataDirective, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[MetadataDirective]:
    return crud.helpers.read_by_values(db_table=MetadataDirective, values=values, db=db)


def update(uuid: UUID, model: MetadataDirectiveUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=MetadataDirective, db=db)
