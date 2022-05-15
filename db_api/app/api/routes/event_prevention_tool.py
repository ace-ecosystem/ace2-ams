from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
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
from exceptions.db import UuidNotFoundInDatabase


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
    obj = crud.event_prevention_tool.create_or_read(model=create, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_prevention_tool", uuid=obj.uuid)


helpers.api_route_create(router, create_event_prevention_tool)


#
# READ
#


def get_all_event_prevention_tools(db: Session = Depends(get_db)):
    return paginate(
        conn=db, query=crud.helpers.build_read_all_query(EventPreventionTool).order_by(EventPreventionTool.value)
    )


def get_event_prevention_tool(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_prevention_tool.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


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
    try:
        if not crud.helpers.update(uuid=uuid, update_model=event_prevention_tool, db_table=EventPreventionTool, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update event prevention_tool {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    response.headers["Content-Location"] = request.url_for("get_event_prevention_tool", uuid=uuid)


helpers.api_route_update(router, update_event_prevention_tool)


#
# DELETE
#


def delete_event_prevention_tool(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=EventPreventionTool, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete event prevention_tool {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_delete(router, delete_event_prevention_tool)
