from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.threat_type import (
    ThreatTypeCreate,
    ThreatTypeRead,
    ThreatTypeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.threat_type import ThreatType
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/threat/type",
    tags=["Threat Type"],
)


#
# CREATE
#


def create_threat_type(
    create: ThreatTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.threat_type.create_or_read(model=create, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_threat_type", uuid=obj.uuid)


helpers.api_route_create(router, create_threat_type)


#
# READ
#


def get_all_threat_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.threat_type.build_read_all_query())


def get_threat_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.threat_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_threat_types, ThreatTypeRead)
helpers.api_route_read(router, get_threat_type, ThreatTypeRead)


#
# UPDATE
#


def update_threat_type(
    uuid: UUID,
    threat_type: ThreatTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=threat_type, db_table=ThreatType, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update threat type {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_threat_type", uuid=uuid)


helpers.api_route_update(router, update_threat_type)


#
# DELETE
#


def delete_threat_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=ThreatType, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete threat type {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_threat_type)
