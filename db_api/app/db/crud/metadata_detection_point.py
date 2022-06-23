from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.metadata_detection_point import MetadataDetectionPointCreate, MetadataDetectionPointUpdate
from db import crud
from db.schemas.metadata_detection_point import MetadataDetectionPoint


def build_read_all_query() -> Select:
    return select(MetadataDetectionPoint).order_by(MetadataDetectionPoint.value)


def create_or_read(model: MetadataDetectionPointCreate, db: Session) -> MetadataDetectionPoint:
    obj = MetadataDetectionPoint(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=MetadataDetectionPoint, db=db)


def read_all(db: Session) -> list[MetadataDetectionPoint]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> MetadataDetectionPoint:
    return crud.helpers.read_by_uuid(db_table=MetadataDetectionPoint, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> MetadataDetectionPoint:
    return crud.helpers.read_by_value(db_table=MetadataDetectionPoint, value=value, db=db)


def update(uuid: UUID, model: MetadataDetectionPointUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=MetadataDetectionPoint, db=db)
