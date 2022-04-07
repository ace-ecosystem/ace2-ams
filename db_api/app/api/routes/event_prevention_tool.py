from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.routes import helpers
from api_models.event_prevention_tool import (
    EventPreventionToolCreate,
    EventPreventionToolRead,
    EventPreventionToolUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.event_prevention_tool import EventPreventionTool
from db.schemas.queue import Queue


router = APIRouter(
    prefix="/event/prevention_tool",
    tags=["Event Prevention Tool"],
)


#
# CREATE
#


def create_event_prevention_tool(
    create: EventPreventionToolCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    queues = crud.read_by_values(values=create.queues, db_table=Queue, db=db)
    obj: EventPreventionTool = crud.create(obj=create, db_table=EventPreventionTool, db=db, exclude=["queues"])
    obj.queues = queues

    response.headers["Content-Location"] = request.url_for("get_event_prevention_tool", uuid=obj.uuid)


helpers.api_route_create(router, create_event_prevention_tool)


#
# READ
#


def get_all_event_prevention_tools(db: Session = Depends(get_db)):
    return paginate(db, select(EventPreventionTool).order_by(EventPreventionTool.value))


def get_event_prevention_tool(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=EventPreventionTool, db=db)


helpers.api_route_read_all(router, get_all_event_prevention_tools, EventPreventionToolRead)
helpers.api_route_read(router, get_event_prevention_tool, EventPreventionToolRead)


#
# UPDATE
#


def update_event_prevention_tool(
    uuid: UUID,
    update: EventPreventionToolUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    db_obj: EventPreventionTool = crud.read(uuid=uuid, db_table=EventPreventionTool, db=db)

    update_data = update.dict(exclude_unset=True)

    if "description" in update_data:
        db_obj.description = update_data["description"]

    if "queues" in update_data:
        db_obj.queues = crud.read_by_values(values=update_data["queues"], db_table=Queue, db=db)

    if "value" in update_data:
        db_obj.value = update_data["value"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_event_prevention_tool", uuid=uuid)


helpers.api_route_update(router, update_event_prevention_tool)


#
# DELETE
#


def delete_event_prevention_tool(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventPreventionTool, db=db)


helpers.api_route_delete(router, delete_event_prevention_tool)
