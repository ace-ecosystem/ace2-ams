from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.analysis_summary_detail import (
    AnalysisSummaryDetailCreate,
    AnalysisSummaryDetailRead,
    AnalysisSummaryDetailUpdate,
)
from db import crud
from db.database import get_db
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/analysis/summary_detail",
    tags=["Analysis Summary Detail"],
)


#
# CREATE
#


def create_analysis_summary_details(
    analysis_summary_details: list[AnalysisSummaryDetailCreate],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    for analysis_summary_detail in analysis_summary_details:
        try:
            obj = crud.analysis_summary_detail.create_or_read(model=analysis_summary_detail, db=db)
        except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

        response.headers["Content-Location"] = request.url_for("get_analysis_summary_detail", uuid=obj.uuid)

    db.commit()


helpers.api_route_create(router, create_analysis_summary_details)


#
# READ
#


def get_analysis_summary_detail(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.analysis_summary_detail.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis summary detail {uuid} does not exist"
        ) from e


helpers.api_route_read(router, get_analysis_summary_detail, AnalysisSummaryDetailRead)


#
# UPDATE
#


def update_analysis_summary_detail(
    uuid: UUID,
    analysis_summary_detail: AnalysisSummaryDetailUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.analysis_summary_detail.update(uuid=uuid, model=analysis_summary_detail, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update analysis summary detail {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_analysis_summary_detail", uuid=uuid)


helpers.api_route_update(router, update_analysis_summary_detail)


#
# DELETE
#


def delete_analysis_summary_detail(uuid: UUID, db: Session = Depends(get_db)):
    try:
        crud.analysis_summary_detail.delete(uuid=uuid, db=db)
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_analysis_summary_detail)
