from sqlalchemy.orm import Session

from api_models.queue import QueueCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.queue.create_or_read(model=QueueCreate(value=value), db=db)
