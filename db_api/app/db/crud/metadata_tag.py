from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.metadata_tag import MetadataTagCreate, MetadataTagUpdate
from db import crud
from db.schemas.metadata_tag import MetadataTag


def build_read_all_query() -> Select:
    return select(MetadataTag).order_by(MetadataTag.value)


def create_or_read(model: MetadataTagCreate, db: Session) -> MetadataTag:
    obj = MetadataTag(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=MetadataTag, db=db)


def read_all(db: Session) -> list[MetadataTag]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> MetadataTag:
    return crud.helpers.read_by_uuid(db_table=MetadataTag, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> MetadataTag:
    return crud.helpers.read_by_value(db_table=MetadataTag, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[MetadataTag]:
    return crud.helpers.read_by_values(db_table=MetadataTag, values=values, db=db)


def update(uuid: UUID, model: MetadataTagUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=MetadataTag, db=db)
