from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.event_prevention_tool import (
    EventPreventionToolCreate,
    EventPreventionToolRead,
    EventPreventionToolUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.event_prevention_tool import EventPreventionTool


router = APIRouter(
    prefix="/event/prevention_tool",
    tags=["Event Prevention Tool"],
)


#
# CREATE
#


def create_event_prevention_tool(
    event_prevention_tool: EventPreventionToolCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=event_prevention_tool, db_table=EventPreventionTool, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_prevention_tool", uuid=uuid)


helpers.api_route_create(router, create_event_prevention_tool)


#
# READ
#


def get_all_event_prevention_tools(db: Session = Depends(get_db)):
    return paginate(db, select(EventPreventionTool))


def get_event_prevention_tool(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=EventPreventionTool, db=db)


helpers.api_route_read_all(router, get_all_event_prevention_tools, EventPreventionToolRead)
helpers.api_route_read(router, get_event_prevention_tool, EventPreventionToolRead)


#
# UPDATE
#


def update_event_prevention_tool(
    uuid: UUID,
    event_prevention_tool: EventPreventionToolUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=event_prevention_tool, db_table=EventPreventionTool, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_prevention_tool", uuid=uuid)


helpers.api_route_update(router, update_event_prevention_tool)


#
# DELETE
#


def delete_event_prevention_tool(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventPreventionTool, db=db)


helpers.api_route_delete(router, delete_event_prevention_tool)
