from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.queue import QueueCreate
from db import crud
from db.schemas.queue import Queue


def create(model: QueueCreate, db: Session) -> Queue:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = Queue(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> Queue:
    return crud.helpers.read_by_uuid(db_table=Queue, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[Queue]:
    return crud.helpers.read_by_value(db_table=Queue, value=value, db=db)
