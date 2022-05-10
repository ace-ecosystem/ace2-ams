from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta

from api_models.node import NodeCreate
from db import crud
from db.schemas.node import Node


def create(
    model: NodeCreate,
    db_node_type: DeclarativeMeta,
    db: Session,
    exclude: dict = None,
) -> DeclarativeMeta:
    obj: Node = db_node_type(**model.dict(exclude=exclude))

    if hasattr(model, "directives") and model.directives:
        obj.directives = crud.node_directive.read_by_values(values=model.directives, db=db)

    if hasattr(model, "tags") and model.tags:
        obj.tags = crud.node_tag.read_by_values(values=model.tags, db=db)

    if hasattr(model, "threat_actors") and model.threat_actors:
        obj.threat_actors = crud.node_threat_actor.read_by_values(values=model.threat_actors, db=db)

    if hasattr(model, "threats") and model.threats:
        obj.threats = crud.node_threat.read_by_values(values=model.threats, db=db)

    return obj
