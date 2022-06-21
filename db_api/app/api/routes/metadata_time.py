from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.metadata_time import (
    MetadataTimeCreate,
    MetadataTimeRead,
    MetadataTimeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.metadata_time import MetadataTime
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/metadata/time",
    tags=["Time"],
)


#
# CREATE
#


def create_time(
    create: MetadataTimeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.metadata_time.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_time", uuid=obj.uuid)


helpers.api_route_create(router, create_time)


#
# READ
#


def get_time(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.metadata_time.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read(router, get_time, MetadataTimeRead)


#
# UPDATE
#


def update_time(
    uuid: UUID,
    time: MetadataTimeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=time, db_table=MetadataTime, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update time {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_time", uuid=uuid)


helpers.api_route_update(router, update_time)


#
# DELETE
#


def delete_time(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=MetadataTime, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete time {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_time)
