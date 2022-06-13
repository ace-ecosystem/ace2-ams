from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.event_severity import (
    EventSeverityCreate,
    EventSeverityRead,
    EventSeverityUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.event_severity import EventSeverity
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/event/severity",
    tags=["Event Severity"],
)


#
# CREATE
#


def create_event_severity(
    create: EventSeverityCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.event_severity.create_or_read(model=create, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_severity", uuid=obj.uuid)


helpers.api_route_create(router, create_event_severity)


#
# READ
#


def get_all_event_severitys(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.event_severity.build_read_all_query())


def get_event_severity(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_severity.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_event_severitys, EventSeverityRead)
helpers.api_route_read(router, get_event_severity, EventSeverityRead)


#
# UPDATE
#


def update_event_severity(
    uuid: UUID,
    event_severity: EventSeverityUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=event_severity, db_table=EventSeverity, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update event severity {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_severity", uuid=uuid)


helpers.api_route_update(router, update_event_severity)


#
# DELETE
#


def delete_event_severity(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=EventSeverity, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete event severity {uuid}"
            )
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_event_severity)
