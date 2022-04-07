from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.routes import helpers
from api_models.node_threat_actor import (
    NodeThreatActorCreate,
    NodeThreatActorRead,
    NodeThreatActorUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.node_threat_actor import NodeThreatActor
from db.schemas.queue import Queue


router = APIRouter(
    prefix="/node/threat_actor",
    tags=["Node Threat Actor"],
)


#
# CREATE
#


def create_node_threat_actor(
    create: NodeThreatActorCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    queues = crud.read_by_values(values=create.queues, db_table=Queue, db=db)
    obj: NodeThreatActor = crud.create(obj=create, db_table=NodeThreatActor, db=db, exclude=["queues"])
    obj.queues = queues

    response.headers["Content-Location"] = request.url_for("get_node_threat_actor", uuid=obj.uuid)


helpers.api_route_create(router, create_node_threat_actor)


#
# READ
#


def get_all_node_threat_actors(db: Session = Depends(get_db)):
    return paginate(db, select(NodeThreatActor).order_by(NodeThreatActor.value))


def get_node_threat_actor(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeThreatActor, db=db)


helpers.api_route_read_all(router, get_all_node_threat_actors, NodeThreatActorRead)
helpers.api_route_read(router, get_node_threat_actor, NodeThreatActorRead)


#
# UPDATE
#


def update_node_threat_actor(
    uuid: UUID,
    update: NodeThreatActorUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    db_obj: NodeThreatActor = crud.read(uuid=uuid, db_table=NodeThreatActor, db=db)

    update_data = update.dict(exclude_unset=True)

    if "description" in update_data:
        db_obj.description = update_data["description"]

    if "queues" in update_data:
        db_obj.queues = crud.read_by_values(values=update_data["queues"], db_table=Queue, db=db)

    if "value" in update_data:
        db_obj.value = update_data["value"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_node_threat_actor", uuid=uuid)


helpers.api_route_update(router, update_node_threat_actor)


#
# DELETE
#


def delete_node_threat_actor(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeThreatActor, db=db)


helpers.api_route_delete(router, delete_node_threat_actor)
