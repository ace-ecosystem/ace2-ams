from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.event_risk_level import (
    EventRiskLevelCreate,
    EventRiskLevelRead,
    EventRiskLevelUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.event_risk_level import EventRiskLevel
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/event/risk_level",
    tags=["Event Risk Level"],
)


#
# CREATE
#


def create_event_risk_level(
    create: EventRiskLevelCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.event_risk_level.create_or_read(model=create, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_risk_level", uuid=obj.uuid)


helpers.api_route_create(router, create_event_risk_level)


#
# READ
#


def get_all_event_risk_levels(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(EventRiskLevel).order_by(EventRiskLevel.value))


def get_event_risk_level(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_risk_level.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_event_risk_levels, EventRiskLevelRead)
helpers.api_route_read(router, get_event_risk_level, EventRiskLevelRead)


#
# UPDATE
#


def update_event_risk_level(
    uuid: UUID,
    event_risk_level: EventRiskLevelUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=event_risk_level, db_table=EventRiskLevel, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update event risk_level {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    response.headers["Content-Location"] = request.url_for("get_event_risk_level", uuid=uuid)


helpers.api_route_update(router, update_event_risk_level)


#
# DELETE
#


def delete_event_risk_level(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=EventRiskLevel, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete event risk_level {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_delete(router, delete_event_risk_level)
