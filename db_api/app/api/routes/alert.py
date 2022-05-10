from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from api.routes import helpers
from api_models.alert import AlertCreate, AlertRead, AlertUpdate
from api_models.create import Create
from api_models.history import AlertHistoryRead
from db import crud
from db.database import get_db
from db.schemas.alert import AlertHistory


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
    alert = crud.alert.create(model=alert, db=db)

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=alert.uuid)

    return {"uuid": alert.uuid}


helpers.api_route_create(router, create_alert, response_model=Create)


#
# READ
#


def get_all_alerts(
    db: Session = Depends(get_db),
    alert_type: Optional[str] = None,
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
    observable: Optional[str] = Query(None, regex="^[\w\-]+\|.+$"),  # type|value
    observable_types: Optional[str] = None,
    observable_value: Optional[str] = None,
    owner: Optional[str] = None,
    queue: Optional[str] = None,
    sort: Optional[str] = Query(
        None,
        regex=""
        "^("
        "(disposition)|"
        "(disposition_time)|"
        "(disposition_user)|"
        "(event_time)|"
        "(insert_time)|"
        "(name)|"
        "(owner)|"
        "(queue)|"
        "(type)"
        ")\|"
        "("
        "(asc)|"
        "(desc)"
        ")$",
    ),  # Example: event_time|desc,
    tags: Optional[str] = None,
    threat_actors: Optional[str] = None,
    threats: Optional[str] = None,
    tool: Optional[str] = None,
    tool_instance: Optional[str] = None,
):
    return paginate(
        conn=db,
        query=crud.alert.build_read_all_query(
            alert_type=alert_type,
            disposition=disposition,
            disposition_user=disposition_user,
            dispositioned_after=dispositioned_after,
            dispositioned_before=dispositioned_before,
            event_uuid=event_uuid,
            event_time_after=event_time_after,
            event_time_before=event_time_before,
            insert_time_after=insert_time_after,
            insert_time_before=insert_time_before,
            name=name,
            observable=observable,
            observable_types=observable_types,
            observable_value=observable_value,
            owner=owner,
            queue=queue,
            sort=sort,
            tags=tags,
            threat_actors=threat_actors,
            threats=threats,
            tool=tool,
            tool_instance=tool_instance,
        ),
    )


def get_alert(uuid: UUID, db: Session = Depends(get_db)):
    alert_tree = crud.alert.read_tree(uuid=uuid, db=db)

    if alert_tree is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert {uuid} does not exist")

    return alert_tree


def get_alert_history(uuid: UUID, db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.history.build_read_history_query(history_table=AlertHistory, record_uuid=uuid))


helpers.api_route_read_all(router, get_all_alerts, AlertRead)
helpers.api_route_read(router, get_alert, dict)
helpers.api_route_read_all(router, get_alert_history, AlertHistoryRead, path="/{uuid}/history")


#
# UPDATE
#


def update_alerts(
    alerts: List[AlertUpdate],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    for alert in alerts:
        crud.alert.update(model=alert, db=db)

        response.headers["Content-Location"] = request.url_for("get_alert", uuid=alert.uuid)


helpers.api_route_update(router, update_alerts, path="/")


#
# DELETE
#


# We currently do not support deleting any Nodes.
