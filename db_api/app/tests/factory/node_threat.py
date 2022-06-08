from sqlalchemy.orm import Session
from typing import Optional

from api_models.node_threat import NodeThreatCreate
from api_models.node_threat_type import NodeThreatTypeCreate
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
        crud.node_threat_type.create_or_read(model=NodeThreatTypeCreate(queues=queues, value=type), db=db)

    return crud.node_threat.create_or_read(
        model=NodeThreatCreate(description=description, queues=queues, types=types, value=value), db=db
    )
