from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.metadata_display_type import MetadataDisplayTypeCreate, MetadataDisplayTypeUpdate
from db import crud
from db.schemas.metadata_display_type import MetadataDisplayType


def build_read_all_query() -> Select:
    return select(MetadataDisplayType).order_by(MetadataDisplayType.value)


def create_or_read(model: MetadataDisplayTypeCreate, db: Session) -> MetadataDisplayType:
    obj = MetadataDisplayType(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=MetadataDisplayType, db=db)


def read_all(db: Session) -> list[MetadataDisplayType]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> MetadataDisplayType:
    return crud.helpers.read_by_uuid(db_table=MetadataDisplayType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> MetadataDisplayType:
    return crud.helpers.read_by_value(db_table=MetadataDisplayType, value=value, db=db)


def update(uuid: UUID, model: MetadataDisplayTypeUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=MetadataDisplayType, db=db)
