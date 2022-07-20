from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.metadata_critical_point import MetadataCriticalPointCreate, MetadataCriticalPointUpdate
from db import crud
from db.schemas.metadata_critical_point import MetadataCriticalPoint


def build_read_all_query() -> Select:
    return select(MetadataCriticalPoint).order_by(MetadataCriticalPoint.value)


def create_or_read(model: MetadataCriticalPointCreate, db: Session) -> MetadataCriticalPoint:
    obj = MetadataCriticalPoint(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=MetadataCriticalPoint, db=db)


def read_all(db: Session) -> list[MetadataCriticalPoint]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> MetadataCriticalPoint:
    return crud.helpers.read_by_uuid(db_table=MetadataCriticalPoint, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> MetadataCriticalPoint:
    return crud.helpers.read_by_value(db_table=MetadataCriticalPoint, value=value, db=db)


def update(uuid: UUID, model: MetadataCriticalPointUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=MetadataCriticalPoint, db=db)
