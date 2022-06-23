from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.metadata_detection_point import (
    MetadataDetectionPointCreate,
    MetadataDetectionPointRead,
    MetadataDetectionPointUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.metadata_detection_point import MetadataDetectionPoint
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/metadata/detection_point",
    tags=["Detection Point"],
)


#
# CREATE
#


def create_detection_point(
    create: MetadataDetectionPointCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.metadata_detection_point.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_detection_point", uuid=obj.uuid)


helpers.api_route_create(router, create_detection_point, response_model=Create)


#
# READ
#


def get_all_detection_points(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.metadata_detection_point.build_read_all_query())


def get_detection_point(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.metadata_detection_point.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_detection_points, MetadataDetectionPointRead)
helpers.api_route_read(router, get_detection_point, MetadataDetectionPointRead)


#
# UPDATE
#


def update_detection_point(
    uuid: UUID,
    detection_point: MetadataDetectionPointUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=detection_point, db_table=MetadataDetectionPoint, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update detection point {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_detection_point", uuid=uuid)


helpers.api_route_update(router, update_detection_point)


#
# DELETE
#


def delete_detection_point(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=MetadataDetectionPoint, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete detection point {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_detection_point)
