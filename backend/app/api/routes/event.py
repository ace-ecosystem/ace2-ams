from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from typing import List, Optional
from uuid import UUID

from api.models.event import EventCreate, EventRead, EventUpdateMultiple
from api.routes import helpers
from api.routes.node import create_node, update_node
from db import crud
from db.database import get_db
from db.schemas.alert import Alert
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.event import Event
from db.schemas.event_prevention_tool import EventPreventionTool
from db.schemas.event_queue import EventQueue
from db.schemas.event_remediation import EventRemediation
from db.schemas.event_risk_level import EventRiskLevel
from db.schemas.event_source import EventSource
from db.schemas.event_status import EventStatus
from db.schemas.event_type import EventType
from db.schemas.event_vector import EventVector
from db.schemas.node import Node
from db.schemas.node_tag import NodeTag
from db.schemas.node_tag_mapping import node_tag_mapping
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_mapping import node_threat_mapping
from db.schemas.node_threat_actor import NodeThreatActor
from db.schemas.node_threat_actor_mapping import node_threat_actor_mapping
from db.schemas.node_tree import NodeTree
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType
from db.schemas.user import User


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
    # Create the new event Node using the data from the request
    new_event: Event = create_node(node_create=event, db_node_type=Event, db=db, exclude={"alert_uuids"})

    # Set the required event properties
    new_event.queue = crud.read_by_value(value=event.queue, db_table=EventQueue, db=db)
    new_event.status = crud.read_by_value(value=event.status, db_table=EventStatus, db=db)

    # Set the various optional event properties if they were given in the request.
    if event.owner:
        new_event.owner = crud.read_user_by_username(username=event.owner, db=db)

    if event.prevention_tools:
        new_event.prevention_tools = crud.read_by_values(
            values=event.prevention_tools,
            db_table=EventPreventionTool,
            db=db,
        )

    if event.remediations:
        new_event.remediations = crud.read_by_values(values=event.remediations, db_table=EventRemediation, db=db)

    if event.risk_level:
        new_event.risk_level = crud.read_by_value(value=event.risk_level, db_table=EventRiskLevel, db=db)

    if event.source:
        new_event.source = crud.read_by_value(value=event.source, db_table=EventSource, db=db)

    if event.type:
        new_event.type = crud.read_by_value(value=event.type, db_table=EventType, db=db)

    if event.vectors:
        new_event.vectors = crud.read_by_values(values=event.vectors, db_table=EventVector, db=db)

    # Save the new event to the database
    db.add(new_event)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_event", uuid=new_event.uuid)


helpers.api_route_create(router, create_event)


#
# READ
#


def _join_as_subquery(query: select, subquery: select):
    s = subquery.subquery()
    return query.join(s, Event.uuid == s.c.uuid).group_by(Event.uuid, Node.uuid)


def get_all_events(
    db: Session = Depends(get_db),
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
    source: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[str] = None,
    threat_actors: Optional[str] = None,
    threats: Optional[str] = None,
    type: Optional[str] = None,
    vectors: Optional[str] = None,
):
    query = select(Event)

    if alert_time_after:
        alert_time_after_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .where(or_(Event.alert_time > alert_time_after, Alert.insert_time > alert_time_after))
        )
        query = _join_as_subquery(query, alert_time_after_query)

    if alert_time_before:
        alert_time_before_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .where(Alert.insert_time < alert_time_before)
        )
        query = _join_as_subquery(query, alert_time_before_query)

    if contain_time_after:
        contain_time_after_query = select(Event).where(Event.contain_time > contain_time_after)
        query = _join_as_subquery(query, contain_time_after_query)

    if contain_time_before:
        contain_time_before_query = select(Event).where(Event.contain_time < contain_time_before)
        query = _join_as_subquery(query, contain_time_before_query)

    if created_time_after:
        created_time_after_query = select(Event).where(Event.creation_time > created_time_after)
        query = _join_as_subquery(query, created_time_after_query)

    if created_time_before:
        created_time_before_query = select(Event).where(Event.creation_time < created_time_before)
        query = _join_as_subquery(query, created_time_before_query)

    if disposition:
        disposition_query = select(Event).join(Alert, onclause=Alert.event_uuid == Event.uuid)
        if disposition.lower() == "none":
            disposition_query = disposition_query.where(
                Alert.disposition_uuid == None  # pylint: disable=singleton-comparison
            )
        else:
            disposition_query = disposition_query.join(AlertDisposition).where(AlertDisposition.value == disposition)

        query = _join_as_subquery(query, disposition_query)

    if disposition_time_after:
        disposition_time_after_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .where(Alert.disposition_time > disposition_time_after)
        )
        query = _join_as_subquery(query, disposition_time_after_query)

    if disposition_time_before:
        disposition_time_before_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .where(Alert.disposition_time < disposition_time_before)
        )
        query = _join_as_subquery(query, disposition_time_before_query)

    if name:
        name_query = select(Event).where(Event.name.ilike(f"%{name}%"))
        query = _join_as_subquery(query, name_query)

    if observable:
        observable_split = observable.split("|", maxsplit=1)
        observable_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(Observable, onclause=Observable.uuid == NodeTree.node_uuid)
            .join(ObservableType)
            .where(ObservableType.value == observable_split[0], Observable.value == observable_split[1])
        )

        query = _join_as_subquery(query, observable_query)

    if observable_types:
        type_filters = [func.count(1).filter(ObservableType.value == t) > 0 for t in observable_types.split(",")]
        observable_types_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(Observable, onclause=Observable.uuid == NodeTree.node_uuid)
            .join(ObservableType)
            .having(and_(*type_filters))
            .group_by(Event.uuid, Node.uuid)
        )

        query = _join_as_subquery(query, observable_types_query)

    if observable_value:
        observable_value_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(Observable, onclause=Observable.uuid == NodeTree.node_uuid)
            .where(Observable.value == observable_value)
        )

        query = _join_as_subquery(query, observable_value_query)

    if owner:
        owner_query = select(Event).join(User, onclause=Event.owner_uuid == User.uuid).where(User.username == owner)
        query = _join_as_subquery(query, owner_query)

    if prevention_tools:
        prevention_tool_filters = []
        for prevention_tool in prevention_tools.split(","):
            prevention_tool_filters.append(Event.prevention_tools.any(EventPreventionTool.value == prevention_tool))

        prevention_tools_query = select(Event).where(and_(*prevention_tool_filters))
        query = _join_as_subquery(query, prevention_tools_query)

    if queue:
        queue_query = select(Event).join(EventQueue).where(EventQueue.value == queue)
        query = _join_as_subquery(query, queue_query)

    if remediation_time_after:
        remediation_time_after_query = select(Event).where(Event.remediation_time > remediation_time_after)
        query = _join_as_subquery(query, remediation_time_after_query)

    if remediation_time_before:
        remediation_time_before_query = select(Event).where(Event.remediation_time < remediation_time_before)
        query = _join_as_subquery(query, remediation_time_before_query)

    if remediations:
        remediation_filters = []
        for remediation in remediations.split(","):
            remediation_filters.append(Event.remediations.any(EventRemediation.value == remediation))

        remediations_query = select(Event).where(and_(*remediation_filters))
        query = _join_as_subquery(query, remediations_query)

    if risk_level:
        risk_level_query = select(Event).join(EventRiskLevel).where(EventRiskLevel.value == risk_level)
        query = _join_as_subquery(query, risk_level_query)

    if source:
        source_query = select(Event).join(EventSource).where(EventSource.value == source)
        query = _join_as_subquery(query, source_query)

    if status:
        status_query = select(Event).join(EventStatus).where(EventStatus.value == status)
        query = _join_as_subquery(query, status_query)

    if tags:
        tag_filters = [func.count(1).filter(NodeTag.value == t) > 0 for t in tags.split(",")]
        tags_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(
                node_tag_mapping,
                onclause=or_(
                    node_tag_mapping.c.node_uuid == Event.uuid, node_tag_mapping.c.node_uuid == NodeTree.node_uuid
                ),
            )
            .join(NodeTag, onclause=NodeTag.uuid == node_tag_mapping.c.tag_uuid)
            .having(and_(*tag_filters))
            .group_by(Event.uuid, Node.uuid)
        )

        query = _join_as_subquery(query, tags_query)

    if threat_actors:
        threat_actor_filters = [func.count(1).filter(NodeThreatActor.value == t) > 0 for t in threat_actors.split(",")]
        threat_actor_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(
                node_threat_actor_mapping,
                onclause=or_(
                    node_threat_actor_mapping.c.node_uuid == Event.uuid,
                    node_threat_actor_mapping.c.node_uuid == NodeTree.node_uuid,
                ),
            )
            .join(NodeThreatActor, onclause=NodeThreatActor.uuid == node_threat_actor_mapping.c.threat_actor_uuid)
            .having(and_(*threat_actor_filters))
            .group_by(Event.uuid, Node.uuid)
        )

        query = _join_as_subquery(query, threat_actor_query)

    if threats:
        threat_filters = [func.count(1).filter(NodeThreat.value == t) > 0 for t in threats.split(",")]
        threat_query = (
            select(Event)
            .join(Alert, onclause=Alert.event_uuid == Event.uuid)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(
                node_threat_mapping,
                onclause=or_(
                    node_threat_mapping.c.node_uuid == Event.uuid,
                    node_threat_mapping.c.node_uuid == NodeTree.node_uuid,
                ),
            )
            .join(NodeThreat, onclause=NodeThreat.uuid == node_threat_mapping.c.threat_uuid)
            .having(and_(*threat_filters))
            .group_by(Event.uuid, Node.uuid)
        )

        query = _join_as_subquery(query, threat_query)

    if type:
        type_query = select(Event).join(EventType).where(EventType.value == type)
        query = _join_as_subquery(query, type_query)

    if vectors:
        vector_filters = []
        for vector in vectors.split(","):
            vector_filters.append(Event.vectors.any(EventVector.value == vector))

        vectors_query = select(Event).where(and_(*vector_filters))
        query = _join_as_subquery(query, vectors_query)

    return paginate(db, query)


def get_event(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=Event, db=db)


helpers.api_route_read_all(router, get_all_events, EventRead)
helpers.api_route_read(router, get_event, EventRead)


#
# UPDATE
#


def update_events(
    events: List[EventUpdateMultiple],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    for event in events:
        # Update the Node attributes
        db_event: Event = update_node(node_update=event, uuid=event.uuid, db_table=Event, db=db)

        # Get the data that was given in the request and use it to update the database object
        update_data = event.dict(exclude_unset=True)

        if "alert_time" in update_data:
            db_event.alert_time = update_data["alert_time"]

        if "contain_time" in update_data:
            db_event.contain_time = update_data["contain_time"]

        if "disposition_time" in update_data:
            db_event.disposition_time = update_data["disposition_time"]

        if "event_time" in update_data:
            db_event.event_time = update_data["event_time"]

        if "name" in update_data:
            db_event.name = update_data["name"]

        if "owner" in update_data:
            db_event.owner = crud.read_user_by_username(username=update_data["owner"], db=db)

        if "ownership_time" in update_data:
            db_event.ownership_time = update_data["ownership_time"]

        if "prevention_tools" in update_data:
            db_event.prevention_tools = crud.read_by_values(
                values=update_data["prevention_tools"],
                db_table=EventPreventionTool,
                db=db,
            )

        if "queue" in update_data:
            db_event.queue = crud.read_by_value(value=update_data["queue"], db_table=EventQueue, db=db)

        if "remediation_time" in update_data:
            db_event.remediation_time = update_data["remediation_time"]

        if "remediations" in update_data:
            db_event.remediations = crud.read_by_values(
                values=update_data["remediations"],
                db_table=EventRemediation,
                db=db,
            )

        if "risk_level" in update_data:
            db_event.risk_level = crud.read_by_value(value=update_data["risk_level"], db_table=EventRiskLevel, db=db)

        if "source" in update_data:
            db_event.source = crud.read_by_value(value=update_data["source"], db_table=EventSource, db=db)

        if "status" in update_data:
            db_event.status = crud.read_by_value(value=update_data["status"], db_table=EventStatus, db=db)

        if "type" in update_data:
            db_event.type = crud.read_by_value(value=update_data["type"], db_table=EventType, db=db)

        if "vectors" in update_data:
            db_event.vectors = crud.read_by_values(values=update_data["vectors"], db_table=EventVector, db=db)

        crud.commit(db)

        response.headers["Content-Location"] = request.url_for("get_event", uuid=event.uuid)


helpers.api_route_update(router, update_events, path="/")


#
# DELETE
#


# We currently do not support deleting any Nodes.
