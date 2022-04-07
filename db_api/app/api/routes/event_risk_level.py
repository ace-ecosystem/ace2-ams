from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.routes import helpers
from api_models.event_risk_level import (
    EventRiskLevelCreate,
    EventRiskLevelRead,
    EventRiskLevelUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.queue import Queue
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
    queues = crud.read_by_values(values=create.queues, db_table=Queue, db=db)
    obj: EventRiskLevel = crud.create(obj=create, db_table=EventRiskLevel, db=db, exclude=["queues"])
    obj.queues = queues

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
    update: EventRiskLevelUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    db_obj: EventRiskLevel = crud.read(uuid=uuid, db_table=EventRiskLevel, db=db)

    update_data = update.dict(exclude_unset=True)

    if "description" in update_data:
        db_obj.description = update_data["description"]

    if "queues" in update_data:
        db_obj.queues = crud.read_by_values(values=update_data["queues"], db_table=Queue, db=db)

    if "value" in update_data:
        db_obj.value = update_data["value"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_event_risk_level", uuid=uuid)


helpers.api_route_update(router, update_event_risk_level)


#
# DELETE
#


def delete_event_risk_level(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventRiskLevel, db=db)


helpers.api_route_delete(router, delete_event_risk_level)
