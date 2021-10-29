from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.models.event_source import (
    EventSourceCreate,
    EventSourceRead,
    EventSourceUpdate,
)
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.event_source import EventSource


router = APIRouter(
    prefix="/event/source",
    tags=["Event Source"],
)


#
# CREATE
#


def create_event_source(
    event_source: EventSourceCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=event_source, db_table=EventSource, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_source", uuid=uuid)


helpers.api_route_create(router, create_event_source)


#
# READ
#


def get_all_event_sources(db: Session = Depends(get_db)):
    return crud.read_all(db_table=EventSource, db=db)


def get_event_source(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=EventSource, db=db)


helpers.api_route_read_all(router, get_all_event_sources, List[EventSourceRead])
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
    crud.update(uuid=uuid, obj=event_source, db_table=EventSource, db=db)

    response.headers["Content-Location"] = request.url_for("get_event_source", uuid=uuid)


helpers.api_route_update(router, update_event_source)


#
# DELETE
#


def delete_event_source(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=EventSource, db=db)


helpers.api_route_delete(router, delete_event_source)
