from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.metadata_sort import MetadataSortCreate, MetadataSortUpdate
from db import crud
from db.schemas.metadata_sort import MetadataSort


def build_read_all_query() -> Select:
    return select(MetadataSort).order_by(MetadataSort.value)


def create_or_read(model: MetadataSortCreate, db: Session) -> MetadataSort:
    obj = MetadataSort(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=MetadataSort, db=db)


def read_all(db: Session) -> list[MetadataSort]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> MetadataSort:
    return crud.helpers.read_by_uuid(db_table=MetadataSort, uuid=uuid, db=db)


def read_by_value(value: int, db: Session) -> MetadataSort:
    return crud.helpers.read_by_value(db_table=MetadataSort, value=value, db=db)


def update(uuid: UUID, model: MetadataSortUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=MetadataSort, db=db)
