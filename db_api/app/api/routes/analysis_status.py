from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.analysis_status import (
    AnalysisStatusCreate,
    AnalysisStatusRead,
    AnalysisStatusUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.analysis_status import AnalysisStatus
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/analysis/status",
    tags=["Analysis Status"],
)


#
# CREATE
#


def create_analysis_status(
    create: AnalysisStatusCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.analysis_status.create_or_read(model=create, db=db)
    db.commit()

    response.headers["Content-Location"] = request.url_for("get_analysis_status", uuid=obj.uuid)


helpers.api_route_create(router, create_analysis_status)


#
# READ
#


def get_all_analysis_statuses(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.analysis_status.build_read_all_query())


def get_analysis_status(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.analysis_status.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_analysis_statuses, AnalysisStatusRead)
helpers.api_route_read(router, get_analysis_status, AnalysisStatusRead)


#
# UPDATE
#


def update_analysis_status(
    uuid: UUID,
    type: AnalysisStatusUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=type, db_table=AnalysisStatus, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update analysis status {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_analysis_status", uuid=uuid)


helpers.api_route_update(router, update_analysis_status)


#
# DELETE
#


def delete_analysis_status(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=AnalysisStatus, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete analysis status {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_analysis_status)
