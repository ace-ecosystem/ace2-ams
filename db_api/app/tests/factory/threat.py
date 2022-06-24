from sqlalchemy.orm import Session
from typing import Optional

from api_models.threat import ThreatCreate
from api_models.threat_type import ThreatTypeCreate
from api_models.queue import QueueCreate
from db import crud


def create_or_read(
    value: str, db: Session, description: Optional[str] = None, queues: list[str] = None, types: list[str] = None
):
    if queues is None:
        queues = ["external"]

    for queue in queues:
        crud.queue.create_or_read(model=QueueCreate(value=queue), db=db)

    if types is None:
        types = ["test_type"]

    for type in types:
        crud.threat_type.create_or_read(model=ThreatTypeCreate(queues=queues, value=type), db=db)

    return crud.threat.create_or_read(
        model=ThreatCreate(description=description, queues=queues, types=types, value=value), db=db
    )
