import json

from datetime import datetime
from fastapi import APIRouter, Query, Request, Response, status
from typing import Optional
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.alert import AlertCreate, AlertRead, AlertUpdate
from api_models.history import AlertHistoryRead
from api_models.observable import ObservableRead


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
):
    result = db_api.post(path="/alert/", payload=json.loads(alert.json()))

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=result["uuid"])


helpers.api_route_create(router, create_alert)


#
# READ
#


def get_all_alerts(
    limit: Optional[int] = Query(50, le=100),
    offset: Optional[int] = Query(0),
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
        "(alert_type)|"
        "(disposition)|"
        "(disposition_time)|"
        "(disposition_user)|"
        "(event_time)|"
        "(insert_time)|"
        "(name)|"
        "(owner)|"
        "(queue)"
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
    query_params = f"?limit={limit}&offset={offset}"

    if alert_type:
        query_params += f"&alert_type={alert_type}"

    if disposition:
        query_params += f"&disposition={disposition}"

    if disposition_user:
        query_params += f"&disposition_user={disposition_user}"

    if dispositioned_after:
        query_params += f"&dispositioned_after={dispositioned_after}"

    if dispositioned_before:
        query_params += f"&dispositioned_before={dispositioned_before}"

    if event_time_after:
        query_params += f"&event_time_after={event_time_after}"

    if event_time_before:
        query_params += f"&event_time_before={event_time_before}"

    if event_uuid:
        query_params += f"&event_uuid={event_uuid}"

    if insert_time_after:
        query_params += f"&insert_time_after={insert_time_after}"

    if insert_time_before:
        query_params += f"&insert_time_before={insert_time_before}"

    if name:
        query_params += f"&name={name}"

    if observable:
        query_params += f"&observable={observable}"

    if observable_types:
        query_params += f"&observable_types={observable_types}"

    if observable_value:
        query_params += f"&observable_value={observable_value}"

    if owner:
        query_params += f"&owner={owner}"

    if queue:
        query_params += f"&queue={queue}"

    if tags:
        query_params += f"&tags={tags}"

    if threat_actors:
        query_params += f"&threat_actors={threat_actors}"

    if threats:
        query_params += f"&threats={threats}"

    if tool:
        query_params += f"&tool={tool}"

    if tool_instance:
        query_params += f"&tool_instance={tool_instance}"

    if sort:
        query_params += f"&sort={sort}"

    return db_api.get(path=f"/alert/{query_params}")


def get_alert(uuid: UUID):
    return db_api.get(path=f"/alert/{uuid}")


def get_alert_history(uuid: UUID, limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    query_params = f"?limit={limit}&offset={offset}"
    return db_api.get(f"/alert/{uuid}/history{query_params}")


def get_alerts_observables(uuids: list[UUID]):
    return db_api.post(path="/alert/observables", payload=[str(u) for u in uuids], expected_status=status.HTTP_200_OK)


helpers.api_route_read_all(router, get_all_alerts, AlertRead)
helpers.api_route_read(router, get_alert, dict)
helpers.api_route_read_all(router, get_alert_history, AlertHistoryRead, path="/{uuid}/history")
helpers.api_route_read(router, get_alerts_observables, list[ObservableRead], methods=["POST"], path="/observables")


#
# UPDATE
#


def update_alerts(
    alerts: list[AlertUpdate],
    request: Request,
    response: Response,
):
    db_api.patch(path="/alert/", payload=[json.loads(a.json(exclude_unset=True)) for a in alerts])

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=alerts[-1].uuid)


helpers.api_route_update(router, update_alerts, path="/")
