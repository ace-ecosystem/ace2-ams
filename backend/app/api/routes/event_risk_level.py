from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.event_risk_level import (
    EventRiskLevelCreate,
    EventRiskLevelRead,
    EventRiskLevelUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.event_risk_level import EventRiskLevel


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
    obj: EventRiskLevel = crud.create(obj=create, db_table=EventRiskLevel, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_risk_level", uuid=obj.uuid)


helpers.api_route_create(router, create_event_risk_level)


#
# READ
#


def get_all_event_risk_levels(db: Session = Depends(get_db)):
    return paginate(db, select(EventRiskLevel).order_by(EventRiskLevel.value))


def get_event_risk_level(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=EventRiskLevel, db=db)


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
    crud.update(uuid=uuid, obj=event_risk_level, db_table=EventRiskLevel, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_risk_level", uuid=uuid)


helpers.api_route_update(router, update_event_risk_level)


#
# DELETE
#


def delete_event_risk_level(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventRiskLevel, db=db)


helpers.api_route_delete(router, delete_event_risk_level)
