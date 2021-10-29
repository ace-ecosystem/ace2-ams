from datetime import datetime
from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID, uuid4

from api.models.alert import AlertCreate, AlertRead, AlertUpdate
from api.models.analysis import AnalysisCreate
from api.routes import helpers
from api.routes.node import create_node, update_node
from core.auth import validate_access_token
from db import crud
from db.database import get_db
from db.schemas.alert import Alert
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.alert_queue import AlertQueue
from db.schemas.alert_tool import AlertTool
from db.schemas.alert_tool_instance import AlertToolInstance
from db.schemas.alert_type import AlertType
from db.schemas.analysis import Analysis
from db.schemas.event import Event
from db.schemas.user import User


router = APIRouter(
    prefix="/alert",
    tags=["Alert"],
)


#
# CREATE
#


def create_alert(
    alert: AlertCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Create the new alert Node using the data from the request
    new_alert: Alert = create_node(node_create=alert, db_node_type=Alert, db=db)

    # Set the required alert properties
    new_alert.queue = crud.read_by_value(value=alert.queue, db_table=AlertQueue, db=db)
    new_alert.type = crud.read_by_value(value=alert.type, db_table=AlertType, db=db)

    # Set the various optional alert properties if they were given in the request.
    if alert.owner:
        new_alert.owner = crud.read_user_by_username(username=alert.owner, db=db)

    if alert.tool:
        new_alert.tool = crud.read_by_value(value=alert.tool, db_table=AlertTool, db=db)

    if alert.tool_instance:
        new_alert.tool_instance = crud.read_by_value(value=alert.tool_instance, db_table=AlertToolInstance, db=db)

    # Alerts must point to an Analysis, so if we get this far without any errors, a new Analysis needs to be created.
    new_alert.analysis = create_node(node_create=AnalysisCreate(), db_node_type=Analysis, db=db)

    # Save the new alert (including the new analysis) to the database
    db.add(new_alert)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=new_alert.uuid)


helpers.api_route_create(router, create_alert)


#
# READ
#


def get_all_alerts(
    db: Session = Depends(get_db),
    disposition: Optional[str] = None,
    disposition_user: Optional[str] = None,
    dispositioned_after: Optional[datetime] = None,
    dispositioned_before: Optional[datetime] = None,
    event_uuid: Optional[UUID] = None,
    event_time_after: Optional[datetime] = None,
    event_time_before: Optional[datetime] = None,
    insert_time_after: Optional[datetime] = None,
    insert_time_before: Optional[datetime] = None,
    name: Optional[str] = None,
    owner: Optional[str] = None,
    queue: Optional[str] = None,
    tool: Optional[str] = None,
    tool_instance: Optional[str] = None,
    type: Optional[str] = None,
):
    query = select(Alert)

    if disposition:
        if disposition.lower() == "none":
            query = query.where(Alert.disposition_uuid == None)  # pylint: disable=singleton-comparison
        else:
            query = query.join(AlertDisposition).where(AlertDisposition.value == disposition)

    if disposition_user:
        query = query.join(User, onclause=Alert.disposition_user_uuid == User.uuid).where(
            User.username == disposition_user
        )

    if dispositioned_after:
        query = query.where(Alert.disposition_time > dispositioned_after)

    if dispositioned_before:
        query = query.where(Alert.disposition_time < dispositioned_before)

    if event_time_after:
        query = query.where(Alert.event_time > event_time_after)

    if event_time_before:
        query = query.where(Alert.event_time < event_time_before)

    if event_uuid:
        query = query.join(Event, onclause=Alert.event_uuid == Event.uuid).where(Event.uuid == event_uuid)

    if insert_time_after:
        query = query.where(Alert.insert_time > insert_time_after)

    if insert_time_before:
        query = query.where(Alert.insert_time < insert_time_before)

    if name:
        query = query.where(Alert.name.ilike(f"%{name}%"))

    if owner:
        query = query.join(User, onclause=Alert.owner_uuid == User.uuid).where(User.username == owner)

    if queue:
        query = query.join(AlertQueue).where(AlertQueue.value == queue)

    if tool:
        query = query.join(AlertTool).where(AlertTool.value == tool)

    if tool_instance:
        query = query.join(AlertToolInstance).where(AlertToolInstance.value == tool_instance)

    if type:
        query = query.join(AlertType).where(AlertType.value == type)

    results = paginate(db, query)

    return results


def get_alert(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Alert, db=db)


# It does not make sense to have a get_all_alerts route at this point (and certainly not without pagination).
helpers.api_route_read_all(router, get_all_alerts, LimitOffsetPage[AlertRead])
helpers.api_route_read(router, get_alert, AlertRead)


#
# UPDATE
#


def update_alert(
    uuid: UUID,
    alert: AlertUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    username: str = Depends(validate_access_token),
):
    # Update the Node attributes
    db_alert: Alert = update_node(node_update=alert, uuid=uuid, db_table=Alert, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = alert.dict(exclude_unset=True)

    if "description" in update_data:
        db_alert.description = update_data["description"]

    if "disposition" in update_data:
        db_alert.disposition = crud.read_by_value(value=update_data["disposition"], db_table=AlertDisposition, db=db)
        db_alert.disposition_time = datetime.utcnow()
        db_alert.disposition_user = crud.read_user_by_username(username=username, db=db)

    if "event_uuid" in update_data:
        db_alert.event = crud.read(uuid=update_data["event_uuid"], db_table=Event, db=db)

        # This counts as editing the event, so it should receive a new version.
        db_alert.event.version = uuid4()

    if "event_time" in update_data:
        db_alert.event_time = update_data["event_time"]

    if "instructions" in update_data:
        db_alert.instructions = update_data["instructions"]

    if "name" in update_data:
        db_alert.name = update_data["name"]

    if "owner" in update_data:
        db_alert.owner = crud.read_user_by_username(username=update_data["owner"], db=db)

    if "queue" in update_data:
        db_alert.queue = crud.read_by_value(value=update_data["queue"], db_table=AlertQueue, db=db)

    if "tool" in update_data:
        db_alert.tool = crud.read_by_value(value=update_data["tool"], db_table=AlertTool, db=db)

    if "tool_instance" in update_data:
        db_alert.tool_instance = crud.read_by_value(
            value=update_data["tool_instance"],
            db_table=AlertToolInstance,
            db=db,
        )

    if "type" in update_data:
        db_alert.type = crud.read_by_value(value=update_data["type"], db_table=AlertType, db=db)

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=uuid)


helpers.api_route_update(router, update_alert)


#
# DELETE
#


# We currently do not support deleting any Nodes.
