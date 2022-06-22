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
        for alert_type_item in alert_type:
            query_params += f"&submission_type={alert_type_item}"

    if disposition:
        for disposition_item in disposition:
            query_params += f"&disposition={disposition_item}"

    if disposition_user:
        for disposition_user_item in disposition_user:
            query_params += f"&disposition_user={disposition_user_item}"

    if dispositioned_after:
        for dispositioned_after_item in dispositioned_after:
            query_params += f"&dispositioned_after={dispositioned_after_item}"

    if dispositioned_before:
        for dispositioned_before_item in dispositioned_before:
            query_params += f"&dispositioned_before={dispositioned_before_item}"

    if event_time_after:
        for event_time_after_item in event_time_after:
            query_params += f"&event_time_after={event_time_after_item}"

    if event_time_before:
        for event_time_before_item in event_time_before:
            query_params += f"&event_time_before={event_time_before_item}"

    if event_uuid:
        for event_uuid_item in event_uuid:
            query_params += f"&event_uuid={event_uuid_item}"

    if insert_time_after:
        for insert_time_after_item in insert_time_after:
            query_params += f"&insert_time_after={insert_time_after_item}"

    if insert_time_before:
        for insert_time_before_item in insert_time_before:
            query_params += f"&insert_time_before={insert_time_before_item}"

    if name:
        for name_item in name:
            query_params += f"&name={name_item}"

    if not_alert_type:
        for not_alert_type_item in not_alert_type:
            query_params += f"&not_submission_type={not_alert_type_item}"

    if not_disposition:
        for not_disposition_item in not_disposition:
            query_params += f"&not_disposition={not_disposition_item}"

    if not_disposition_user:
        for not_disposition_user_item in not_disposition_user:
            query_params += f"&not_disposition_user={not_disposition_user_item}"

    if not_event_uuid:
        for not_event_uuid_item in not_event_uuid:
            query_params += f"&not_event_uuid={not_event_uuid_item}"

    if not_name:
        for not_name_item in not_name:
            query_params += f"&not_name={not_name_item}"

    if not_observable:
        for not_observable_item in not_observable:
            query_params += f"&not_observable={not_observable_item}"

    if not_observable_types:
        for not_observable_types_item in not_observable_types:
            query_params += f"&not_observable_types={not_observable_types_item}"

    if not_observable_value:
        for not_observable_value_item in not_observable_value:
            query_params += f"&not_observable_value={not_observable_value_item}"

    if not_owner:
        for not_owner_item in not_owner:
            query_params += f"&not_owner={not_owner_item}"

    if not_queue:
        for not_queue_item in not_queue:
            query_params += f"&not_queue={not_queue_item}"

    if not_tags:
        for not_tags_item in not_tags:
            query_params += f"&not_tags={not_tags_item}"

    if not_tool:
        for not_tool_item in not_tool:
            query_params += f"&not_tool={not_tool_item}"

    if not_tool_instance:
        for not_tool_instance_item in not_tool_instance:
            query_params += f"&not_tool_instance={not_tool_instance_item}"

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

    if queue:
        for queue_item in queue:
            query_params += f"&queue={queue_item}"

    if tags:
        for tags_item in tags:
            query_params += f"&tags={tags_item}"

    if threat_actors:
        for threat_actors_item in threat_actors:
            query_params += f"&threat_actors={threat_actors_item}"

    if threats:
        for threats_item in threats:
            query_params += f"&threats={threats_item}"

    if tool:
        for tool_item in tool:
            query_params += f"&tool={tool_item}"

    if tool_instance:
        for tool_instance_item in tool_instance:
            query_params += f"&tool_instance={tool_instance_item}"

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
