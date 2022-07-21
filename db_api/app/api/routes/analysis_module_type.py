from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.analysis_module_type import (
    AnalysisModuleTypeCreate,
    AnalysisModuleTypeRead,
    AnalysisModuleTypeUpdate,
)
from db import crud
from db.database import get_db
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/analysis/module_type",
    tags=["Analysis Module Type"],
)


#
# CREATE
#


def create_analysis_module_type(
    analysis_module_type: AnalysisModuleTypeCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.analysis_module_type.create_or_read(model=analysis_module_type, db=db)

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_analysis_module_type", uuid=obj.uuid)


helpers.api_route_create(router, create_analysis_module_type)


#
# READ
#


def get_all_analysis_module_types(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.analysis_module_type.build_read_all_query())


def get_analysis_module_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.analysis_module_type.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis module type {uuid} does not exist"
        ) from e


helpers.api_route_read_all(router, get_all_analysis_module_types, AnalysisModuleTypeRead)
helpers.api_route_read(router, get_analysis_module_type, AnalysisModuleTypeRead)


#
# UPDATE
#


def update_analysis_module_type(
    uuid: UUID,
    analysis_module_type: AnalysisModuleTypeUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.analysis_module_type.update(uuid=uuid, model=analysis_module_type, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update analysis module type {uuid}"
            )
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_analysis_module_type", uuid=uuid)


helpers.api_route_update(router, update_analysis_module_type)


#
# DELETE
#


def delete_analysis_module_type(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.analysis_module_type.delete(uuid=uuid, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete analysis module type {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_analysis_module_type)
