from sqlalchemy.orm import Session

from api_models.event_remediation import EventRemediationCreate
from api_models.queue import QueueCreate
from db import crud


def create(value: str, db: Session, queues: list[str] = None):
    if queues is None:
        queues = ["external"]

    for queue in queues:
        crud.queue.create_or_read(model=QueueCreate(value=queue), db=db)

    return crud.event_remediation.create_or_read(model=EventRemediationCreate(queues=queues, value=value), db=db)