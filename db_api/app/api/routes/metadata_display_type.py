from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.metadata_display_type import (
    MetadataDisplayTypeCreate,
    MetadataDisplayTypeRead,
    MetadataDisplayTypeUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.metadata_display_type import MetadataDisplayType
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/metadata/display_type",
    tags=["Display Type"],
)


#
# CREATE
#


def create_display_type(
    create: MetadataDisplayTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.metadata_display_type.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_display_type", uuid=obj.uuid)

    return {"uuid": obj.uuid}


helpers.api_route_create(router, create_display_type, response_model=Create)


#
# READ
#


def get_all_display_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.metadata_display_type.build_read_all_query())


def get_display_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.metadata_display_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_display_types, MetadataDisplayTypeRead)
helpers.api_route_read(router, get_display_type, MetadataDisplayTypeRead)


#
# UPDATE
#


def update_display_type(
    uuid: UUID,
    display_type: MetadataDisplayTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=display_type, db_table=MetadataDisplayType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update metadata display type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_display_type", uuid=uuid)


helpers.api_route_update(router, update_display_type)


#
# DELETE
#


def delete_display_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=MetadataDisplayType, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete metadata display type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_display_type)
