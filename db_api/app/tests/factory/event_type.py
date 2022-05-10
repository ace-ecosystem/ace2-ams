from sqlalchemy.orm import Session

from api_models.event_type import EventTypeCreate
from api_models.queue import QueueCreate
from db import crud


def create(value: str, db: Session, queues: list[str] = None):
    if queues is None:
        queues = ["external"]

    for queue in queues:
        crud.queue.create(model=QueueCreate(value=queue), db=db)

    return crud.event_type.create(model=EventTypeCreate(queues=queues, value=value), db=db)
