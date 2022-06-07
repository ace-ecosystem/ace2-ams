from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.queue import QueueCreate, QueueUpdate
from db import crud
from db.schemas.queue import Queue


def build_read_all_query() -> Select:
    return select(Queue).order_by(Queue.value)


def create_or_read(model: QueueCreate, db: Session) -> Queue:
    obj = Queue(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=Queue, db=db)


def read_all(db: Session) -> list[Queue]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> Queue:
    return crud.helpers.read_by_uuid(db_table=Queue, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Queue:
    return crud.helpers.read_by_value(db_table=Queue, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[Queue]:
    return crud.helpers.read_by_values(db_table=Queue, values=values, db=db)


def update(uuid: UUID, model: QueueUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=Queue, db=db)
