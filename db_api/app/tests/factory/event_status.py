from sqlalchemy.orm import Session
from typing import Optional

from api_models.event_status import EventStatusCreate
from api_models.queue import QueueCreate
from db import crud


def create_or_read(value: str, db: Session, description: Optional[str] = None, queues: list[str] = None):
    if queues is None:
        queues = ["external"]

    for queue in queues:
        crud.queue.create_or_read(model=QueueCreate(value=queue), db=db)

    return crud.event_status.create_or_read(
        model=EventStatusCreate(description=description, queues=queues, value=value), db=db
    )
