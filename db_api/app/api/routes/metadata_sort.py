from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.metadata_sort import (
    MetadataSortCreate,
    MetadataSortRead,
    MetadataSortUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.metadata_sort import MetadataSort
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/metadata/sort",
    tags=["Sort"],
)


#
# CREATE
#


def create_sort(
    create: MetadataSortCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.metadata_sort.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_sort", uuid=obj.uuid)


helpers.api_route_create(router, create_sort)


#
# READ
#


def get_all_sorts(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.metadata_sort.build_read_all_query())


def get_sort(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.metadata_sort.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_sorts, MetadataSortRead)
helpers.api_route_read(router, get_sort, MetadataSortRead)


#
# UPDATE
#


def update_sort(
    uuid: UUID,
    sort: MetadataSortUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=sort, db_table=MetadataSort, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update sort {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_sort", uuid=uuid)


helpers.api_route_update(router, update_sort)


#
# DELETE
#


def delete_sort(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=MetadataSort, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete sort {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_sort)
