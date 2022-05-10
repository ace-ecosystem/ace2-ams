from sqlalchemy.orm import Session

from api_models.node_threat import NodeThreatCreate
from api_models.node_threat_type import NodeThreatTypeCreate
from api_models.queue import QueueCreate
from db import crud


def create(value: str, db: Session, queues: list[str] = None, types: list[str] = None):
    if queues is None:
        queues = ["external"]

    for queue in queues:
        crud.queue.create(model=QueueCreate(value=queue), db=db)

    if types is None:
        types = ["test_type"]

    for type in types:
        crud.node_threat_type.create(model=NodeThreatTypeCreate(queues=queues, value=type), db=db)

    return crud.node_threat.create(model=NodeThreatCreate(queues=queues, types=types, value=value), db=db)
