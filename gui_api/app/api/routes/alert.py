import json
import requests

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from typing import List, Optional
from uuid import UUID

from api_models.alert import AlertCreate, AlertRead, AlertUpdateMultiple
from api_models.history import AlertHistoryRead
from api.routes import helpers

from core.auth import validate_access_token
from core.config import get_settings


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
    claims: dict = Depends(validate_access_token),
):
    try:
        result = requests.post(
            f"{get_settings().database_api_url}/alert/?history_username={claims['sub']}", json=json.loads(alert.json())
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=result.json()["uuid"])


helpers.api_route_create(router, create_alert)


#
# READ
#


def get_all_alerts(
    limit: Optional[int] = Query(50, le=100),
    offset: Optional[int] = Query(0),
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
    type: Optional[str] = None,
):
    query_params = f"?limit={limit}&offset={offset}"

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

    if type:
        query_params += f"&type={type}"

    if sort:
        query_params += f"&sort={sort}"

    try:
        result = requests.get(
            f"{get_settings().database_api_url}/alert/{query_params}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result.json()


def get_alert(uuid: UUID):
    try:
        result = requests.get(
            f"{get_settings().database_api_url}/alert/{uuid}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result.json()


def get_alert_history(uuid: UUID):
    try:
        result = requests.get(
            f"{get_settings().database_api_url}/alert/{uuid}/history",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result.json()


helpers.api_route_read_all(router, get_all_alerts, AlertRead)
helpers.api_route_read(router, get_alert, dict)
helpers.api_route_read_all(router, get_alert_history, AlertHistoryRead, path="/{uuid}/history")


#
# UPDATE
#


def update_alerts(
    alerts: List[AlertUpdateMultiple],
    request: Request,
    response: Response,
    claims: dict = Depends(validate_access_token),
):
    try:
        result = requests.patch(
            f"{get_settings().database_api_url}/alert/?history_username={claims['sub']}",
            json=[json.loads(a.json(exclude_unset=True)) for a in alerts],
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if result.status_code == status.HTTP_204_NO_CONTENT:
        response.headers["Content-Location"] = request.url_for("get_alert", uuid=alerts[-1].uuid)


helpers.api_route_update(router, update_alerts, path="/")
