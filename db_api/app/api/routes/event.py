from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.create import Create
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
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.event import EventHistory
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase, VersionMismatch


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
    try:
        event = crud.event.create_or_read(model=event, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event", uuid=event.uuid)

    return {"uuid": event.uuid}


helpers.api_route_create(router, create_event, response_model=Create)


#
# READ
#


def get_all_events(
    db: Session = Depends(get_db),
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
        "(status)"
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
    return paginate(
        conn=db,
        query=crud.event.build_read_all_query(
            alert_time_after=alert_time_after,
            alert_time_before=alert_time_before,
            contain_time_after=contain_time_after,
            contain_time_before=contain_time_before,
            created_time_after=created_time_after,
            created_time_before=created_time_before,
            disposition=disposition,
            disposition_time_after=disposition_time_after,
            disposition_time_before=disposition_time_before,
            event_type=event_type,
            name=name,
            not_disposition=not_disposition,
            not_event_type=not_event_type,
            not_name=not_name,
            not_observable=not_observable,
            not_observable_types=not_observable_types,
            not_observable_value=not_observable_value,
            not_owner=not_owner,
            not_prevention_tools=not_prevention_tools,
            not_queue=not_queue,
            not_remediations=not_remediations,
            not_severity=not_severity,
            not_source=not_source,
            not_status=not_status,
            not_tags=not_tags,
            not_threat_actors=not_threat_actors,
            not_threats=not_threats,
            not_vectors=not_vectors,
            observable=observable,
            observable_types=observable_types,
            observable_value=observable_value,
            owner=owner,
            prevention_tools=prevention_tools,
            queue=queue,
            remediation_time_after=remediation_time_after,
            remediation_time_before=remediation_time_before,
            remediations=remediations,
            severity=severity,
            sort=sort,
            source=source,
            status=status,
            tags=tags,
            threat_actors=threat_actors,
            threats=threats,
            vectors=vectors,
        ),
    )


def get_event(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event.read_by_uuid(uuid=uuid, db=db, inject_analysis_types=True)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {uuid} does not exist") from e


def get_event_history(uuid: UUID, db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.history.build_read_history_query(history_table=EventHistory, record_uuid=uuid))


helpers.api_route_read_all(router, get_all_events, EventRead)
helpers.api_route_read(router, get_event, EventRead)
helpers.api_route_read_all(router, get_event_history, EventHistoryRead, path="/{uuid}/history")


#
# UPDATE
#


def update_events(
    events: list[EventUpdateMultiple],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    for event in events:
        try:
            crud.event.update(uuid=event.uuid, model=event, db=db)
        except UuidNotFoundInDatabase as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except ValueNotFoundInDatabase as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except VersionMismatch as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

        response.headers["Content-Location"] = request.url_for("get_event", uuid=event.uuid)

    db.commit()


helpers.api_route_update(router, update_events, path="/")


#
# SUMMARIES
#


def get_detection_point_summary(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event.read_summary_detection_point(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {uuid} does not exist") from e


def get_email_headers_body_summary(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event.read_summary_email_headers_body(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {uuid} does not exist") from e


def get_email_summary(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event.read_summary_email(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {uuid} does not exist") from e


def get_observable_summary(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event.read_summary_observable(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {uuid} does not exist") from e


def get_sandbox_summary(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event.read_summary_sandbox(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {uuid} does not exist") from e


def get_url_domain_summary(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event.read_summary_url_domain(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {uuid} does not exist") from e


def get_user_summary(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event.read_summary_user(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event {uuid} does not exist") from e


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
