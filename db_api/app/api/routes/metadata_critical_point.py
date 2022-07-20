from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.metadata_critical_point import (
    MetadataCriticalPointCreate,
    MetadataCriticalPointRead,
    MetadataCriticalPointUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.metadata_critical_point import MetadataCriticalPoint
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/metadata/critical_point",
    tags=["Critical Point"],
)


#
# CREATE
#


def create_critical_point(
    create: MetadataCriticalPointCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.metadata_critical_point.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_critical_point", uuid=obj.uuid)


helpers.api_route_create(router, create_critical_point, response_model=Create)


#
# READ
#


def get_all_critical_points(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.metadata_critical_point.build_read_all_query())


def get_critical_point(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.metadata_critical_point.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_critical_points, MetadataCriticalPointRead)
helpers.api_route_read(router, get_critical_point, MetadataCriticalPointRead)


#
# UPDATE
#


def update_critical_point(
    uuid: UUID,
    critical_point: MetadataCriticalPointUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=critical_point, db_table=MetadataCriticalPoint, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update critical point {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_critical_point", uuid=uuid)


helpers.api_route_update(router, update_critical_point)


#
# DELETE
#


def delete_critical_point(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=MetadataCriticalPoint, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete critical point {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_critical_point)
