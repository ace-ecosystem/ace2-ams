from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.metadata_display_value import (
    MetadataDisplayValueCreate,
    MetadataDisplayValueRead,
    MetadataDisplayValueUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.metadata_display_value import MetadataDisplayValue
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/metadata/display_value",
    tags=["Display Value"],
)


#
# CREATE
#


def create_display_value(
    create: MetadataDisplayValueCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.metadata_display_value.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_display_value", uuid=obj.uuid)

    return {"uuid": obj.uuid}


helpers.api_route_create(router, create_display_value, response_model=Create)


#
# READ
#


def get_all_display_values(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.metadata_display_value.build_read_all_query())


def get_display_value(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.metadata_display_value.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_display_values, MetadataDisplayValueRead)
helpers.api_route_read(router, get_display_value, MetadataDisplayValueRead)


#
# UPDATE
#


def update_display_value(
    uuid: UUID,
    display_value: MetadataDisplayValueUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=display_value, db_table=MetadataDisplayValue, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update metadata display value {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_display_value", uuid=uuid)


helpers.api_route_update(router, update_display_value)


#
# DELETE
#


def delete_display_value(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=MetadataDisplayValue, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete metadata display value {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_display_value)
