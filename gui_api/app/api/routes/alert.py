import json

from datetime import datetime
from fastapi import APIRouter, Query, Request, Response, status
from typing import Optional
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.history import SubmissionHistoryRead
from api_models.observable import ObservableSubmissionRead
from api_models.submission import SubmissionCreate, SubmissionRead, SubmissionUpdate
from api_models.summaries import URLDomainSummary


router = APIRouter(
    prefix="/alert",
    tags=["Alert"],
)


#
# CREATE
#


def create_alert(
    alert: SubmissionCreate,
    request: Request,
    response: Response,
):
    result = db_api.post(path="/submission/", payload=json.loads(alert.json()))

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=result["uuid"])


helpers.api_route_create(router, create_alert)


#
# READ
#


def get_all_alerts(
    limit: Optional[int] = Query(50, le=100),
    offset: Optional[int] = Query(0),
    alert_type: Optional[list[str]] = Query(None),
    disposition: Optional[list[str]] = Query(None),
    disposition_user: Optional[list[str]] = Query(None),
    dispositioned_after: Optional[list[datetime]] = Query(None),
    dispositioned_before: Optional[list[datetime]] = Query(None),
    event_uuid: Optional[list[UUID]] = Query(None),
    event_time_after: Optional[list[datetime]] = Query(None),
    event_time_before: Optional[list[datetime]] = Query(None),
    insert_time_after: Optional[list[datetime]] = Query(None),
    insert_time_before: Optional[list[datetime]] = Query(None),
    name: Optional[list[str]] = Query(None),
    not_alert_type: Optional[list[str]] = Query(None),
    not_disposition: Optional[list[str]] = Query(None),
    not_disposition_user: Optional[list[str]] = Query(None),
    not_event_uuid: Optional[list[UUID]] = Query(None),
    not_name: Optional[list[str]] = Query(None),
    not_observable: Optional[list[str]] = Query(None, regex="^[\w\-]+\|.+$"),  # type|value
    not_observable_types: Optional[list[str]] = Query(None),
    not_observable_value: Optional[list[str]] = Query(None),
    not_owner: Optional[list[str]] = Query(None),
    not_queue: Optional[list[str]] = Query(None),
    not_tags: Optional[list[str]] = Query(None),
    not_tool: Optional[list[str]] = Query(None),
    not_tool_instance: Optional[list[str]] = Query(None),
    observable: Optional[list[str]] = Query(None, regex="^[\w\-]+\|.+$"),  # type|value
    observable_types: Optional[list[str]] = Query(None),
    observable_value: Optional[list[str]] = Query(None),
    owner: Optional[list[str]] = Query(None),
    queue: Optional[list[str]] = Query(None),
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
    tags: Optional[list[str]] = Query(None),
    threat_actors: Optional[list[str]] = Query(None),
    threats: Optional[list[str]] = Query(None),
    tool: Optional[list[str]] = Query(None),
    tool_instance: Optional[list[str]] = Query(None),
):
    # alert=True is hardcoded in the query to the database API so that the GUI only receives
    # submissions that are considered to be alerts.
    query_params = f"?limit={limit}&offset={offset}&alert=True"

    if alert_type:
        for item in alert_type:
            query_params += f"&submission_type={item}"

    if disposition:
        for item in disposition:
            query_params += f"&disposition={item}"

    if disposition_user:
        for item in disposition_user:
            query_params += f"&disposition_user={item}"

    if dispositioned_after:
        for item in dispositioned_after:
            query_params += f"&dispositioned_after={item}"

    if dispositioned_before:
        for item in dispositioned_before:
            query_params += f"&dispositioned_before={item}"

    if event_time_after:
        for item in event_time_after:
            query_params += f"&event_time_after={item}"

    if event_time_before:
        for item in event_time_before:
            query_params += f"&event_time_before={item}"

    if event_uuid:
        for item in event_uuid:
            query_params += f"&event_uuid={item}"

    if insert_time_after:
        for item in insert_time_after:
            query_params += f"&insert_time_after={item}"

    if insert_time_before:
        for item in insert_time_before:
            query_params += f"&insert_time_before={item}"

    if name:
        for item in name:
            query_params += f"&name={item}"

    if not_alert_type:
        for item in not_alert_type:
            query_params += f"&not_submission_type={item}"

    if not_disposition:
        for item in not_disposition:
            query_params += f"&not_disposition={item}"

    if not_disposition_user:
        for item in not_disposition_user:
            query_params += f"&not_disposition_user={item}"

    if not_event_uuid:
        for item in not_event_uuid:
            query_params += f"&not_event_uuid={item}"

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

    if not_queue:
        for item in not_queue:
            query_params += f"&not_queue={item}"

    if not_tags:
        for item in not_tags:
            query_params += f"&not_tags={item}"

    if not_tool:
        for item in not_tool:
            query_params += f"&not_tool={item}"

    if not_tool_instance:
        for item in not_tool_instance:
            query_params += f"&not_tool_instance={item}"

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

    if queue:
        for item in queue:
            query_params += f"&queue={item}"

    if tags:
        for item in tags:
            query_params += f"&tags={item}"

    if threat_actors:
        for item in threat_actors:
            query_params += f"&threat_actors={item}"

    if threats:
        for item in threats:
            query_params += f"&threats={item}"

    if tool:
        for item in tool:
            query_params += f"&tool={item}"

    if tool_instance:
        for item in tool_instance:
            query_params += f"&tool_instance={item}"

    if sort:
        query_params += f"&sort={sort}"

    return db_api.get(path=f"/submission/{query_params}")


def get_alert(uuid: UUID):
    return db_api.get(path=f"/submission/{uuid}")


def get_alert_history(uuid: UUID, limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    query_params = f"?limit={limit}&offset={offset}"
    return db_api.get(f"/submission/{uuid}/history{query_params}")


def get_alerts_observables(uuids: list[UUID]):
    return db_api.post(
        path="/submission/observables", payload=[str(u) for u in uuids], expected_status=status.HTTP_200_OK
    )


helpers.api_route_read_all(router, get_all_alerts, SubmissionRead)
helpers.api_route_read(router, get_alert, dict)
helpers.api_route_read_all(router, get_alert_history, SubmissionHistoryRead, path="/{uuid}/history")
helpers.api_route_read(
    router, get_alerts_observables, list[ObservableSubmissionRead], methods=["POST"], path="/observables"
)


#
# UPDATE
#


def update_alerts(
    alerts: list[SubmissionUpdate],
    request: Request,
    response: Response,
):
    db_api.patch(path="/submission/", payload=[json.loads(a.json(exclude_unset=True)) for a in alerts])

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=alerts[-1].uuid)


helpers.api_route_update(router, update_alerts, path="/")


#
# SUMMARIES
#


def get_url_domain_summary(uuid: UUID):
    return db_api.get(path=f"/submission/{uuid}/summary/url_domain")


helpers.api_route_read(router, get_url_domain_summary, URLDomainSummary, path="/{uuid}/summary/url_domain")
