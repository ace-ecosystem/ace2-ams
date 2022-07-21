from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.format import FormatCreate, FormatRead, FormatUpdate
from db import crud
from db.database import get_db
from db.schemas.format import Format
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/format",
    tags=["Format"],
)


#
# CREATE
#


def create_format(
    create: FormatCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.format.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_format", uuid=obj.uuid)


helpers.api_route_create(router, create_format)


#
# READ
#


def get_all_formats(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.format.build_read_all_query())


def get_format(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.format.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_formats, FormatRead)
helpers.api_route_read(router, get_format, FormatRead)


#
# UPDATE
#


def update_format(
    uuid: UUID,
    observable_relationship: FormatUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=observable_relationship, db_table=Format, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update format {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_format", uuid=uuid)


helpers.api_route_update(router, update_format)


#
# DELETE
#


def delete_format(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=Format, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete format {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_format)
