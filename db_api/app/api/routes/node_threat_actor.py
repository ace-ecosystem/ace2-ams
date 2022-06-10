from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
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
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


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
    try:
        obj = crud.node_threat_actor.create_or_read(model=create, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_threat_actor", uuid=obj.uuid)


helpers.api_route_create(router, create_node_threat_actor)


#
# READ
#


def get_all_node_threat_actors(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.node_threat_actor.build_read_all_query())


def get_node_threat_actor(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.node_threat_actor.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


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
    try:
        if not crud.helpers.update(uuid=uuid, update_model=node_threat_actor, db_table=NodeThreatActor, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update node threat_actor {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_threat_actor", uuid=uuid)


helpers.api_route_update(router, update_node_threat_actor)


#
# DELETE
#


def delete_node_threat_actor(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=NodeThreatActor, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete node threat_actor {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_node_threat_actor)
