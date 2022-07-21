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
    not_disposition: Optional[list[str]] = Query(None),
    not_event_type: Optional[list[str]] = Query(None),
    not_name: Optional[list[str]] = Query(None),
    not_observable: Optional[list[str]] = Query(None),  # type|value
    not_observable_types: Optional[list[str]] = Query(None),
    not_observable_value: Optional[list[str]] = Query(None),
    not_owner: Optional[list[str]] = Query(None),
    not_prevention_tools: Optional[list[str]] = Query(None),
    not_queue: Optional[list[str]] = Query(None),
    not_remediations: Optional[list[str]] = Query(None),
    not_severity: Optional[list[str]] = Query(None),
    not_source: Optional[list[str]] = Query(None),
    not_status: Optional[list[str]] = Query(None),
    not_tags: Optional[list[str]] = Query(None),
    not_threat_actors: Optional[list[str]] = Query(None),
    not_threats: Optional[list[str]] = Query(None),
    not_vectors: Optional[list[str]] = Query(None),
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
        for item in alert_time_after:
            query_params += f"&alert_time_after={item}"

    if alert_time_before:
        for item in alert_time_before:
            query_params += f"&alert_time_before={item}"

    if contain_time_after:
        for item in contain_time_after:
            query_params += f"&contain_time_after={item}"

    if contain_time_before:
        for item in contain_time_before:
            query_params += f"&contain_time_before={item}"

    if created_time_after:
        for item in created_time_after:
            query_params += f"&created_time_after={item}"

    if created_time_before:
        for item in created_time_before:
            query_params += f"&created_time_before={item}"

    if disposition:
        for item in disposition:
            query_params += f"&disposition={item}"

    if disposition_time_after:
        for item in disposition_time_after:
            query_params += f"&disposition_time_after={item}"

    if disposition_time_before:
        for item in disposition_time_before:
            query_params += f"&disposition_time_before={item}"

    if event_type:
        for item in event_type:
            query_params += f"&event_type={item}"

    if name:
        for item in name:
            query_params += f"&name={item}"

    if not_disposition:
        for item in not_disposition:
            query_params += f"&not_disposition={item}"

    if not_event_type:
        for item in not_event_type:
            query_params += f"&not_event_type={item}"

    if not_name:
        for item in not_name:
            query_params += f"&not_name={item}"

    if not_observable:
        for item in not_observable:
            query_params += f"&not_observable={item}"

    if not_observable_types:
        for item in not_observable_types:
            query_params += f"&not_observable_types={item}"

    if not_observable_value:
        for item in not_observable_value:
            query_params += f"&not_observable_value={item}"

    if not_owner:
        for item in not_owner:
            query_params += f"&not_owner={item}"

    if not_prevention_tools:
        for item in not_prevention_tools:
            query_params += f"&not_prevention_tools={item}"

    if not_queue:
        for item in not_queue:
            query_params += f"&not_queue={item}"

    if not_remediations:
        for item in not_remediations:
            query_params += f"&not_remediations={item}"

    if not_severity:
        for item in not_severity:
            query_params += f"&not_severity={item}"

    if not_source:
        for item in not_source:
            query_params += f"&not_source={item}"

    if not_status:
        for item in not_status:
            query_params += f"&not_status={item}"

    if not_tags:
        for item in not_tags:
            query_params += f"&not_tags={item}"

    if not_threat_actors:
        for item in not_threat_actors:
            query_params += f"&not_threat_actors={item}"

    if not_threats:
        for item in not_threats:
            query_params += f"&not_threats={item}"

    if not_vectors:
        for item in not_vectors:
            query_params += f"&not_vectors={item}"

    if observable:
        for item in observable:
            query_params += f"&observable={item}"

    if observable_types:
        for item in observable_types:
            query_params += f"&observable_types={item}"

    if observable_value:
        for item in observable_value:
            query_params += f"&observable_value={item}"

    if owner:
        for item in owner:
            query_params += f"&owner={item}"

    if prevention_tools:
        for item in prevention_tools:
            query_params += f"&prevention_tools={item}"

    if queue:
        for item in queue:
            query_params += f"&queue={item}"

    if remediation_time_after:
        for item in remediation_time_after:
            query_params += f"&remediation_time_after={item}"

    if remediation_time_before:
        for item in remediation_time_before:
            query_params += f"&remediation_time_before={item}"

    if remediations:
        for item in remediations:
            query_params += f"&remediations={item}"

    if severity:
        for item in severity:
            query_params += f"&severity={item}"

    if sort:
        query_params += f"&sort={sort}"

    if source:
        for item in source:
            query_params += f"&source={item}"

    if status:
        for item in status:
            query_params += f"&status={item}"

    if tags:
        for item in tags:
            query_params += f"&tags={item}"

    if threat_actors:
        for item in threat_actors:
            query_params += f"&threat_actors={item}"

    if threats:
        for item in threats:
            query_params += f"&threats={item}"

    if vectors:
        for item in vectors:
            query_params += f"&vectors={item}"

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
