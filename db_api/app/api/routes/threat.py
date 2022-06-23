from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.threat import ThreatCreate, ThreatRead, ThreatUpdate
from db import crud
from db.database import get_db
from db.schemas.threat import Threat
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/threat",
    tags=["Threat"],
)


#
# CREATE
#


def create_threat(
    create: ThreatCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.threat.create_or_read(model=create, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_threat", uuid=obj.uuid)

    return {"uuid": obj.uuid}


helpers.api_route_create(router, create_threat, response_model=Create)


#
# READ
#


def get_all_threats(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.threat.build_read_all_query())


def get_threat(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.threat.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_threats, ThreatRead)
helpers.api_route_read(router, get_threat, ThreatRead)


#
# UPDATE
#


def update_threat(
    uuid: UUID,
    threat: ThreatUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.threat.update(uuid=uuid, model=threat, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update threat {uuid}")
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_threat", uuid=uuid)


helpers.api_route_update(router, update_threat)


#
# DELETE
#


def delete_threat(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=Threat, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete threat {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_threat)
