from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.node_threat_actor import (
    NodeThreatActorCreate,
    NodeThreatActorRead,
    NodeThreatActorUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node_threat_actor import NodeThreatActor


router = APIRouter(
    prefix="/node/threat_actor",
    tags=["Node Threat Actor"],
)


#
# CREATE
#


def create_node_threat_actor(
    node_threat_actor: NodeThreatActorCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=node_threat_actor, db_table=NodeThreatActor, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_threat_actor", uuid=uuid)


helpers.api_route_create(router, create_node_threat_actor)


#
# READ
#


def get_all_node_threat_actors(db: Session = Depends(get_db)):
    return paginate(db, select(NodeThreatActor))


def get_node_threat_actor(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeThreatActor, db=db)


helpers.api_route_read_all(router, get_all_node_threat_actors, NodeThreatActorRead)
helpers.api_route_read(router, get_node_threat_actor, NodeThreatActorRead)


#
# UPDATE
#


def update_node_threat_actor(
    uuid: UUID,
    node_threat_actor: NodeThreatActorUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=node_threat_actor, db_table=NodeThreatActor, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_threat_actor", uuid=uuid)


helpers.api_route_update(router, update_node_threat_actor)


#
# DELETE
#


def delete_node_threat_actor(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeThreatActor, db=db)


helpers.api_route_delete(router, delete_node_threat_actor)
