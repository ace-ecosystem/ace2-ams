from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from typing import List
from uuid import UUID

from api.models.event import EventCreate, EventRead, EventUpdateMultiple
from api.routes import helpers
from api.routes.node import create_node, update_node
from db import crud
from db.database import get_db
from db.schemas.event import Event
from db.schemas.event_prevention_tool import EventPreventionTool
from db.schemas.event_queue import EventQueue
from db.schemas.event_remediation import EventRemediation
from db.schemas.event_risk_level import EventRiskLevel
from db.schemas.event_source import EventSource
from db.schemas.event_status import EventStatus
from db.schemas.event_type import EventType
from db.schemas.event_vector import EventVector


router = APIRouter(
    prefix="/event",
    tags=["Event"],
)


#
# CREATE
#


def create_event(
    event: EventCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Create the new event Node using the data from the request
    new_event: Event = create_node(node_create=event, db_node_type=Event, db=db, exclude={"alert_uuids"})

    # Set the required event properties
    new_event.queue = crud.read_by_value(value=event.queue, db_table=EventQueue, db=db)
    new_event.status = crud.read_by_value(value=event.status, db_table=EventStatus, db=db)

    # Set the various optional event properties if they were given in the request.
    if event.owner:
        new_event.owner = crud.read_user_by_username(username=event.owner, db=db)

    if event.prevention_tools:
        new_event.prevention_tools = crud.read_by_values(
            values=event.prevention_tools,
            db_table=EventPreventionTool,
            db=db,
        )

    if event.remediations:
        new_event.remediations = crud.read_by_values(values=event.remediations, db_table=EventRemediation, db=db)

    if event.risk_level:
        new_event.risk_level = crud.read_by_value(value=event.risk_level, db_table=EventRiskLevel, db=db)

    if event.source:
        new_event.source = crud.read_by_value(value=event.source, db_table=EventSource, db=db)

    if event.type:
        new_event.type = crud.read_by_value(value=event.type, db_table=EventType, db=db)

    if event.vectors:
        new_event.vectors = crud.read_by_values(values=event.vectors, db_table=EventVector, db=db)

    # Save the new event to the database
    db.add(new_event)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_event", uuid=new_event.uuid)


helpers.api_route_create(router, create_event)


#
# READ
#


def get_all_events(db: Session = Depends(get_db)):
    query = select(Event)

    return paginate(db, query)


def get_event(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Event, db=db)


# It does not make sense to have a get_all_events route at this point (and certainly not without pagination).
# helpers.api_route_read_all(router, get_all_events, List[EventRead])
helpers.api_route_read(router, get_event, EventRead)


#
# UPDATE
#


def update_events(
    events: List[EventUpdateMultiple],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    for event in events:
        # Update the Node attributes
        db_event: Event = update_node(node_update=event, uuid=event.uuid, db_table=Event, db=db)

        # Get the data that was given in the request and use it to update the database object
        update_data = event.dict(exclude_unset=True)

        if "alert_time" in update_data:
            db_event.alert_time = update_data["alert_time"]

        if "contain_time" in update_data:
            db_event.contain_time = update_data["contain_time"]

        if "disposition_time" in update_data:
            db_event.disposition_time = update_data["disposition_time"]

        if "event_time" in update_data:
            db_event.event_time = update_data["event_time"]

        if "name" in update_data:
            db_event.name = update_data["name"]

        if "owner" in update_data:
            db_event.owner = crud.read_user_by_username(username=update_data["owner"], db=db)

        if "ownership_time" in update_data:
            db_event.ownership_time = update_data["ownership_time"]

        if "prevention_tools" in update_data:
            db_event.prevention_tools = crud.read_by_values(
                values=update_data["prevention_tools"],
                db_table=EventPreventionTool,
                db=db,
            )

        if "queue" in update_data:
            db_event.queue = crud.read_by_value(value=update_data["queue"], db_table=EventQueue, db=db)

        if "remediation_time" in update_data:
            db_event.remediation_time = update_data["remediation_time"]

        if "remediations" in update_data:
            db_event.remediations = crud.read_by_values(
                values=update_data["remediations"],
                db_table=EventRemediation,
                db=db,
            )

        if "risk_level" in update_data:
            db_event.risk_level = crud.read_by_value(value=update_data["risk_level"], db_table=EventRiskLevel, db=db)

        if "source" in update_data:
            db_event.source = crud.read_by_value(value=update_data["source"], db_table=EventSource, db=db)

        if "status" in update_data:
            db_event.status = crud.read_by_value(value=update_data["status"], db_table=EventStatus, db=db)

        if "type" in update_data:
            db_event.type = crud.read_by_value(value=update_data["type"], db_table=EventType, db=db)

        if "vectors" in update_data:
            db_event.vectors = crud.read_by_values(values=update_data["vectors"], db_table=EventVector, db=db)

        crud.commit(db)

        response.headers["Content-Location"] = request.url_for("get_event", uuid=event.uuid)


helpers.api_route_update(router, update_events, path="/")


#
# DELETE
#


# We currently do not support deleting any Nodes.
