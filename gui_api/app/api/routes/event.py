import json

from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request, Response
from typing import List, Optional
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.event import EventCreate, EventRead, EventUpdateMultiple
from api_models.event_summaries import (
    DetectionSummary,
    EmailHeadersBody,
    EmailSummary,
    ObservableSummary,
    SandboxSummary,
    UserSummary,
    URLDomainSummary,
)
from api_models.history import EventHistoryRead
from core.auth import validate_access_token


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
    claims: dict = Depends(validate_access_token),
):
    result = db_api.post(path=f"/event/?history_username={claims['sub']}", payload=json.loads(event.json()))

    response.headers["Content-Location"] = request.url_for("get_event", uuid=result["uuid"])


helpers.api_route_create(router, create_event)


#
# READ
#


def get_all_events(
    limit: Optional[int] = Query(50, le=100),
    offset: Optional[int] = Query(0),
    alert_time_after: Optional[datetime] = None,
    alert_time_before: Optional[datetime] = None,
    contain_time_after: Optional[datetime] = None,
    contain_time_before: Optional[datetime] = None,
    created_time_after: Optional[datetime] = None,
    created_time_before: Optional[datetime] = None,
    disposition: Optional[str] = None,
    disposition_time_after: Optional[datetime] = None,
    disposition_time_before: Optional[datetime] = None,
    name: Optional[str] = None,
    observable: Optional[str] = Query(None, regex="^[\w\-]+\|.+$"),  # type|value
    observable_types: Optional[str] = None,
    observable_value: Optional[str] = None,
    owner: Optional[str] = None,
    prevention_tools: Optional[str] = None,
    queue: Optional[str] = None,
    remediation_time_after: Optional[datetime] = None,
    remediation_time_before: Optional[datetime] = None,
    remediations: Optional[str] = None,
    risk_level: Optional[str] = None,
    sort: Optional[str] = Query(
        None,
        regex=""
        "^("
        "(created_time)|"
        "(name)|"
        "(owner)|"
        "(risk_level)|"
        "(status)|"
        "(type)|"
        ")\|"
        "("
        "(asc)|"
        "(desc)"
        ")$",
    ),  # Example: created_time|desc,
    source: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[str] = None,
    threat_actors: Optional[str] = None,
    threats: Optional[str] = None,
    type: Optional[str] = None,
    vectors: Optional[str] = None,
):
    query_params = f"?limit={limit}&offset={offset}"

    if alert_time_after:
        query_params += f"&alert_time_after={alert_time_after}"

    if alert_time_before:
        query_params += f"&alert_time_before={alert_time_before}"

    if contain_time_after:
        query_params += f"&contain_time_after={contain_time_after}"

    if contain_time_before:
        query_params += f"&contain_time_before={contain_time_before}"

    if created_time_after:
        query_params += f"&created_time_after={created_time_after}"

    if created_time_before:
        query_params += f"&created_time_before={created_time_before}"

    if disposition:
        query_params += f"&disposition={disposition}"

    if disposition_time_after:
        query_params += f"&disposition_time_after={disposition_time_after}"

    if disposition_time_before:
        query_params += f"&disposition_time_before={disposition_time_before}"

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

    if prevention_tools:
        query_params += f"&prevention_tools={prevention_tools}"

    if queue:
        query_params += f"&queue={queue}"

    if remediation_time_after:
        query_params += f"&remediation_time_after={remediation_time_after}"

    if remediation_time_before:
        query_params += f"&remediation_time_before={remediation_time_before}"

    if remediations:
        query_params += f"&remediations={remediations}"

    if risk_level:
        query_params += f"&risk_level={risk_level}"

    if sort:
        query_params += f"&sort={sort}"

    if source:
        query_params += f"&source={source}"

    if status:
        query_params += f"&status={status}"

    if tags:
        query_params += f"&tags={tags}"

    if threat_actors:
        query_params += f"&threat_actors={threat_actors}"

    if threats:
        query_params += f"&threats={threats}"

    if type:
        query_params += f"&type={type}"

    if vectors:
        query_params += f"&vectors={vectors}"

    return db_api.get(path=f"/event/{query_params}")


def get_event(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}")


def get_event_history(uuid: UUID):
    return db_api.get(f"/event/{uuid}/history")


helpers.api_route_read_all(router, get_all_events, EventRead)
helpers.api_route_read(router, get_event, dict)
helpers.api_route_read_all(router, get_event_history, EventHistoryRead, path="/{uuid}/history")


#
# UPDATE
#


def update_events(
    events: List[EventUpdateMultiple],
    request: Request,
    response: Response,
    claims: dict = Depends(validate_access_token),
):
    db_api.patch(
        path=f"/event/?history_username={claims['sub']}",
        payload=[json.loads(e.json(exclude_unset=True)) for e in events],
    )

    response.headers["Content-Location"] = request.url_for("get_event", uuid=events[-1].uuid)


helpers.api_route_update(router, update_events, path="/")


#
# SUMMARIES
#


def get_detection_point_summary(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}/summary/detection_point")


def get_email_headers_body_summary(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}/summary/email_headers_body")


def get_email_summary(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}/summary/email")


def get_observable_summary(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}/summary/observable")


def get_sandbox_summary(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}/summary/sandbox")


def get_user_summary(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}/summary/user")


def get_url_domain_summary(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}/summary/url_domain")


helpers.api_route_read(
    router, get_detection_point_summary, List[DetectionSummary], path="/{uuid}/summary/detection_point"
)
helpers.api_route_read(
    router, get_email_headers_body_summary, Optional[EmailHeadersBody], path="/{uuid}/summary/email_headers_body"
)
helpers.api_route_read(router, get_email_summary, List[EmailSummary], path="/{uuid}/summary/email")
helpers.api_route_read(router, get_observable_summary, List[ObservableSummary], path="/{uuid}/summary/observable")
helpers.api_route_read(router, get_sandbox_summary, List[SandboxSummary], path="/{uuid}/summary/sandbox")
helpers.api_route_read(router, get_user_summary, List[UserSummary], path="/{uuid}/summary/user")
helpers.api_route_read(router, get_url_domain_summary, URLDomainSummary, path="/{uuid}/summary/url_domain")
