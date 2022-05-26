from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.node_threat import NodeThreatCreate, NodeThreatRead, NodeThreatUpdate
from db import crud
from db.database import get_db
from db.schemas.node_threat import NodeThreat
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/node/threat",
    tags=["Node Threat"],
)


#
# CREATE
#


def create_node_threat(
    create: NodeThreatCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.node_threat.create_or_read(model=create, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=obj.uuid)

    return {"uuid": obj.uuid}


helpers.api_route_create(router, create_node_threat, response_model=Create)


#
# READ
#


def get_all_node_threats(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(NodeThreat).order_by(NodeThreat.value))


def get_node_threat(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.node_threat.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_node_threats, NodeThreatRead)
helpers.api_route_read(router, get_node_threat, NodeThreatRead)


#
# UPDATE
#


def update_node_threat(
    uuid: UUID,
    node_threat: NodeThreatUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.node_threat.update(uuid=uuid, model=node_threat, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update node threat {uuid}")
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_threat", uuid=uuid)


helpers.api_route_update(router, update_node_threat)


#
# DELETE
#


def delete_node_threat(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=NodeThreat, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete node threat {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_node_threat)
