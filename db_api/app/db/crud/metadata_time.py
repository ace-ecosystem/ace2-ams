from datetime import datetime
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.metadata_time import MetadataTimeCreate, MetadataTimeUpdate
from db import crud
from db.schemas.metadata_time import MetadataTime


def create_or_read(model: MetadataTimeCreate, db: Session) -> MetadataTime:
    obj = MetadataTime(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=MetadataTime, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> MetadataTime:
    return crud.helpers.read_by_uuid(db_table=MetadataTime, uuid=uuid, db=db)


def read_by_value(value: datetime, db: Session) -> MetadataTime:
    return crud.helpers.read_by_value(db_table=MetadataTime, value=value, db=db)


def update(uuid: UUID, model: MetadataTimeUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=MetadataTime, db=db)
