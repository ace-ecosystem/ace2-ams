from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.metadata_display_value import MetadataDisplayValueCreate, MetadataDisplayValueUpdate
from db import crud
from db.schemas.metadata_display_value import MetadataDisplayValue


def build_read_all_query() -> Select:
    return select(MetadataDisplayValue).order_by(MetadataDisplayValue.value)


def create_or_read(model: MetadataDisplayValueCreate, db: Session) -> MetadataDisplayValue:
    obj = MetadataDisplayValue(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=MetadataDisplayValue, db=db)


def read_all(db: Session) -> list[MetadataDisplayValue]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> MetadataDisplayValue:
    return crud.helpers.read_by_uuid(db_table=MetadataDisplayValue, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> MetadataDisplayValue:
    return crud.helpers.read_by_value(db_table=MetadataDisplayValue, value=value, db=db)


def update(uuid: UUID, model: MetadataDisplayValueUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=MetadataDisplayValue, db=db)
