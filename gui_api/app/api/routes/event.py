import json

from datetime import datetime
from fastapi import APIRouter, Query, Request, Response
from typing import Optional
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
)
from api_models.summaries import URLDomainSummary
from api_models.history import EventHistoryRead


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
):
    result = db_api.post(path="/event/", payload=json.loads(event.json()))

    response.headers["Content-Location"] = request.url_for("get_event", uuid=result["uuid"])


helpers.api_route_create(router, create_event)


#
# READ
#


def get_all_events(
    limit: Optional[int] = Query(50, le=100),
    offset: Optional[int] = Query(0),
    alert_time_after: Optional[list[datetime]] = Query(None),
    alert_time_before: Optional[list[datetime]] = Query(None),
    contain_time_after: Optional[list[datetime]] = Query(None),
    contain_time_before: Optional[list[datetime]] = Query(None),
    created_time_after: Optional[list[datetime]] = Query(None),
    created_time_before: Optional[list[datetime]] = Query(None),
    disposition: Optional[list[str]] = Query(None),
    disposition_time_after: Optional[list[datetime]] = Query(None),
    disposition_time_before: Optional[list[datetime]] = Query(None),
    event_type: Optional[list[str]] = Query(None),
    name: Optional[list[str]] = Query(None),
    observable: Optional[list[str]] = Query(None, regex="^[\w\-]+\|.+$"),  # type|value
    observable_types: Optional[list[str]] = Query(None),
    observable_value: Optional[list[str]] = Query(None),
    owner: Optional[list[str]] = Query(None),
    prevention_tools: Optional[list[str]] = Query(None),
    queue: Optional[list[str]] = Query(None),
    remediation_time_after: Optional[list[datetime]] = Query(None),
    remediation_time_before: Optional[list[datetime]] = Query(None),
    remediations: Optional[list[str]] = Query(None),
    severity: Optional[list[str]] = Query(None),
    sort: Optional[str] = Query(
        None,
        regex=""
        "^("
        "(created_time)|"
        "(event_type)|"
        "(name)|"
        "(owner)|"
        "(severity)|"
        "(status)|"
        ")\|"
        "("
        "(asc)|"
        "(desc)"
        ")$",
    ),  # Example: created_time|desc,
    source: Optional[list[str]] = Query(None),
    status: Optional[list[str]] = Query(None),
    tags: Optional[list[str]] = Query(None),
    threat_actors: Optional[list[str]] = Query(None),
    threats: Optional[list[str]] = Query(None),
    vectors: Optional[list[str]] = Query(None),
):
    query_params = f"?limit={limit}&offset={offset}"

    if alert_time_after:
        for alert_time_after_item in alert_time_after:
            query_params += f"&alert_time_after={alert_time_after_item}"

    if alert_time_before:
        for alert_time_before_item in alert_time_before:
            query_params += f"&alert_time_before={alert_time_before_item}"

    if contain_time_after:
        for contain_time_after_item in contain_time_after:
            query_params += f"&contain_time_after={contain_time_after_item}"

    if contain_time_before:
        for contain_time_before_item in contain_time_before:
            query_params += f"&contain_time_before={contain_time_before_item}"

    if created_time_after:
        for created_time_after_item in created_time_after:
            query_params += f"&created_time_after={created_time_after_item}"

    if created_time_before:
        for created_time_before_item in created_time_before:
            query_params += f"&created_time_before={created_time_before_item}"

    if disposition:
        for disposition_item in disposition:
            query_params += f"&disposition={disposition_item}"

    if disposition_time_after:
        for disposition_time_after_item in disposition_time_after:
            query_params += f"&disposition_time_after={disposition_time_after_item}"

    if disposition_time_before:
        for disposition_time_before_item in disposition_time_before:
            query_params += f"&disposition_time_before={disposition_time_before_item}"

    if event_type:
        for event_type_item in event_type:
            query_params += f"&event_type={event_type_item}"

    if name:
        for name_item in name:
            query_params += f"&name={name_item}"

    if observable:
        for observable_item in observable:
            query_params += f"&observable={observable_item}"

    if observable_types:
        for observable_types_item in observable_types:
            query_params += f"&observable_types={observable_types_item}"

    if observable_value:
        for observable_value_item in observable_value:
            query_params += f"&observable_value={observable_value_item}"

    if owner:
        for owner_item in owner:
            query_params += f"&owner={owner_item}"

    if prevention_tools:
        for prevention_tools_item in prevention_tools:
            query_params += f"&prevention_tools={prevention_tools_item}"

    if queue:
        for queue_item in queue:
            query_params += f"&queue={queue_item}"

    if remediation_time_after:
        for remediation_time_after_item in remediation_time_after:
            query_params += f"&remediation_time_after={remediation_time_after_item}"

    if remediation_time_before:
        for remediation_time_before_item in remediation_time_before:
            query_params += f"&remediation_time_before={remediation_time_before_item}"

    if remediations:
        for remediations_item in remediations:
            query_params += f"&remediations={remediations_item}"

    if severity:
        for severity_item in severity:
            query_params += f"&severity={severity_item}"

    if sort:
        query_params += f"&sort={sort}"

    if source:
        for source_item in source:
            query_params += f"&source={source_item}"

    if status:
        for status_item in status:
            query_params += f"&status={status_item}"

    if tags:
        for tags_item in tags:
            query_params += f"&tags={tags_item}"

    if threat_actors:
        for threat_actors_item in threat_actors:
            query_params += f"&threat_actors={threat_actors_item}"

    if threats:
        for threats_item in threats:
            query_params += f"&threats={threats_item}"

    if vectors:
        for vectors_item in vectors:
            query_params += f"&vectors={vectors_item}"

    return db_api.get(path=f"/event/{query_params}")


def get_event(uuid: UUID):
    return db_api.get(path=f"/event/{uuid}")


def get_event_history(uuid: UUID, limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    query_params = f"?limit={limit}&offset={offset}"
    return db_api.get(f"/event/{uuid}/history{query_params}")


helpers.api_route_read_all(router, get_all_events, EventRead)
helpers.api_route_read(router, get_event, dict)
helpers.api_route_read_all(router, get_event_history, EventHistoryRead, path="/{uuid}/history")


#
# UPDATE
#


def update_events(
    events: list[EventUpdateMultiple],
    request: Request,
    response: Response,
):
    db_api.patch(path="/event/", payload=[json.loads(e.json(exclude_unset=True)) for e in events])

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
    router, get_detection_point_summary, list[DetectionSummary], path="/{uuid}/summary/detection_point"
)
helpers.api_route_read(
    router, get_email_headers_body_summary, Optional[EmailHeadersBody], path="/{uuid}/summary/email_headers_body"
)
helpers.api_route_read(router, get_email_summary, list[EmailSummary], path="/{uuid}/summary/email")
helpers.api_route_read(router, get_observable_summary, list[ObservableSummary], path="/{uuid}/summary/observable")
helpers.api_route_read(router, get_sandbox_summary, list[SandboxSummary], path="/{uuid}/summary/sandbox")
helpers.api_route_read(router, get_user_summary, list[UserSummary], path="/{uuid}/summary/user")
helpers.api_route_read(router, get_url_domain_summary, URLDomainSummary, path="/{uuid}/summary/url_domain")
