from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.event_source import (
    EventSourceCreate,
    EventSourceRead,
    EventSourceUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.event_source import EventSource
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/event/source",
    tags=["Event Source"],
)


#
# CREATE
#


def create_event_source(
    create: EventSourceCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.event_source.create_or_read(model=create, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_source", uuid=obj.uuid)


helpers.api_route_create(router, create_event_source)


#
# READ
#


def get_all_event_sources(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(EventSource).order_by(EventSource.value))


def get_event_source(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_source.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_event_sources, EventSourceRead)
helpers.api_route_read(router, get_event_source, EventSourceRead)


#
# UPDATE
#


def update_event_source(
    uuid: UUID,
    event_source: EventSourceUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.helpers.update(uuid=uuid, update_model=event_source, db_table=EventSource, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update event source {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_source", uuid=uuid)


helpers.api_route_update(router, update_event_source)


#
# DELETE
#


def delete_event_source(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=EventSource, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete event source {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_event_source)
