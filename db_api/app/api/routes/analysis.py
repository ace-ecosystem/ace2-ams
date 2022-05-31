from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.analysis import AnalysisCreate, AnalysisRead, AnalysisUpdate
from db import crud
from db.database import get_db
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


#
# CREATE
#


def create_analysis(
    analysis: AnalysisCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.analysis.create_or_read(model=analysis, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_analysis", uuid=obj.uuid)


helpers.api_route_create(router, create_analysis)


#
# READ
#


def get_analysis(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.analysis.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis {uuid} does not exist") from e


helpers.api_route_read(router, get_analysis, AnalysisRead)


#
# UPDATE
#


def update_analysis(
    uuid: UUID,
    analysis: AnalysisUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        crud.analysis.update(uuid=uuid, model=analysis, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    response.headers["Content-Location"] = request.url_for("get_analysis", uuid=uuid)

    db.commit()


helpers.api_route_update(router, update_analysis)
