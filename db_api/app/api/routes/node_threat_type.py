from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.node_threat_type import (
    NodeThreatTypeCreate,
    NodeThreatTypeRead,
    NodeThreatTypeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.node_threat_type import NodeThreatType
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/node/threat/type",
    tags=["Node Threat Type"],
)


#
# CREATE
#


def create_node_threat_type(
    create: NodeThreatTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.node_threat_type.create_or_read(model=create, db=db)
        db.commit()
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    response.headers["Content-Location"] = request.url_for("get_node_threat_type", uuid=obj.uuid)


helpers.api_route_create(router, create_node_threat_type)


#
# READ
#


def get_all_node_threat_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(NodeThreatType).order_by(NodeThreatType.value))


def get_node_threat_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.node_threat_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_node_threat_types, NodeThreatTypeRead)
helpers.api_route_read(router, get_node_threat_type, NodeThreatTypeRead)


#
# UPDATE
#


def update_node_threat_type(
    uuid: UUID,
    node_threat_type: NodeThreatTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=node_threat_type, db_table=NodeThreatType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update node threat type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_threat_type", uuid=uuid)


helpers.api_route_update(router, update_node_threat_type)


#
# DELETE
#


def delete_node_threat_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=NodeThreatType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete node threat type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_node_threat_type)
