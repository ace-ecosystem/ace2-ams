from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID, uuid4

from api_models.alert import AlertCreate, AlertRead, AlertUpdateMultiple
from api_models.history import AlertHistoryRead
from api_models.observable import ObservableRead
from api.routes import helpers
from api.routes.node import create_node, update_node
from api.routes.observable import _create_observable
from db import crud
from db.database import get_db
from db.schemas.alert import Alert, AlertHistory
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.alert_tool import AlertTool
from db.schemas.alert_tool_instance import AlertToolInstance
from db.schemas.alert_type import AlertType
from db.schemas.event import Event
from db.schemas.node import Node
from db.schemas.node_tag import NodeTag
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_actor import NodeThreatActor
from db.schemas.node_tree import NodeTree
from db.schemas.observable import Observable, ObservableHistory
from db.schemas.observable_type import ObservableType
from db.schemas.queue import Queue
from db.schemas.user import User


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
    # Create the new alert Node using the data from the request
    new_alert: Alert = create_node(
        node_create=alert,
        db_node_type=Alert,
        db=db,
        exclude={"observables"},
    )

    # Set the required alert properties
    new_alert.queue = crud.read_by_value(value=alert.queue, db_table=Queue, db=db)
    new_alert.type = crud.read_by_value(value=alert.type, db_table=AlertType, db=db)

    # Set the various optional alert properties if they were given in the request.
    if alert.owner:
        new_alert.owner = crud.read_user_by_username(username=alert.owner, db=db)

    if alert.tool:
        new_alert.tool = crud.read_by_value(value=alert.tool, db_table=AlertTool, db=db)

    if alert.tool_instance:
        new_alert.tool_instance = crud.read_by_value(value=alert.tool_instance, db_table=AlertToolInstance, db=db)

    db.add(new_alert)

    crud.commit(db)

    # Add the observables to database
    for observable in alert.observables:
        db_observable = _create_observable(observable, db=db)
        db.add(db_observable)
        observable.uuid = db_observable.uuid

        crud.commit(db)

    # Create a NodeTree with the alert as the root and link the observables to it
    node_tree = crud.create_node_tree_leaf(root_node_uuid=new_alert.uuid, node_uuid=new_alert.uuid, db=db)

    crud.commit(db)

    for observable in alert.observables:
        crud.create_node_tree_leaf(
            root_node_uuid=new_alert.uuid, node_uuid=observable.uuid, parent_tree_uuid=node_tree.uuid, db=db
        )

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_alert", uuid=new_alert.uuid)


helpers.api_route_create(router, create_alert)


#
# READ
#


def _join_as_subquery(query: select, subquery: select):
    s = subquery.subquery()
    return query.join(s, Alert.uuid == s.c.uuid).group_by(Alert.uuid, Node.uuid)


def get_all_alerts(
    db: Session = Depends(get_db),
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
    query = select(Alert)

    if disposition:
        disposition_query = select(Alert)
        if disposition.lower() == "none":
            disposition_query = disposition_query.where(
                Alert.disposition_uuid == None  # pylint: disable=singleton-comparison
            )
        else:
            disposition_query = disposition_query.join(AlertDisposition).where(AlertDisposition.value == disposition)

        query = _join_as_subquery(query, disposition_query)

    if disposition_user:
        disposition_user_query = select(Alert).where(
            Alert.history.any(
                and_(
                    AlertHistory.field == "disposition",
                    AlertHistory.action_by.has(User.username == disposition_user),
                )
            )
        )

        query = _join_as_subquery(query, disposition_user_query)

    if dispositioned_after:
        dispositioned_after_query = select(Alert).where(
            Alert.history.any(and_(AlertHistory.field == "disposition", AlertHistory.action_time > dispositioned_after))
        )
        query = _join_as_subquery(query, dispositioned_after_query)

    if dispositioned_before:
        dispositioned_before_query = select(Alert).where(
            Alert.history.any(
                and_(AlertHistory.field == "disposition", AlertHistory.action_time < dispositioned_before)
            )
        )
        query = _join_as_subquery(query, dispositioned_before_query)

    if event_time_after:
        event_time_after_query = select(Alert).where(Alert.event_time > event_time_after)
        query = _join_as_subquery(query, event_time_after_query)

    if event_time_before:
        event_time_before_query = select(Alert).where(Alert.event_time < event_time_before)
        query = _join_as_subquery(query, event_time_before_query)

    if event_uuid:
        event_uuid_query = (
            select(Alert).join(Event, onclause=Alert.event_uuid == Event.uuid).where(Event.uuid == event_uuid)
        )
        query = _join_as_subquery(query, event_uuid_query)

    if insert_time_after:
        insert_time_after_query = select(Alert).where(Alert.insert_time > insert_time_after)
        query = _join_as_subquery(query, insert_time_after_query)

    if insert_time_before:
        insert_time_before_query = select(Alert).where(Alert.insert_time < insert_time_before)
        query = _join_as_subquery(query, insert_time_before_query)

    if name:
        name_query = select(Alert).where(Alert.name.ilike(f"%{name}%"))
        query = _join_as_subquery(query, name_query)

    if observable:
        observable_split = observable.split("|", maxsplit=1)
        observable_query = (
            select(Alert)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(Observable, onclause=Observable.uuid == NodeTree.node_uuid)
            .join(ObservableType)
            .where(ObservableType.value == observable_split[0], Observable.value == observable_split[1])
        )

        query = _join_as_subquery(query, observable_query)

    if observable_types:
        type_filters = [func.count(1).filter(ObservableType.value == t) > 0 for t in observable_types.split(",")]
        observable_types_query = (
            select(Alert)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(Observable, onclause=Observable.uuid == NodeTree.node_uuid)
            .join(ObservableType)
            .having(and_(*type_filters))
            .group_by(Alert.uuid, Node.uuid)
        )

        query = _join_as_subquery(query, observable_types_query)

    if observable_value:
        observable_value_query = (
            select(Alert)
            .join(NodeTree, onclause=NodeTree.root_node_uuid == Alert.uuid)
            .join(Observable, onclause=Observable.uuid == NodeTree.node_uuid)
            .where(Observable.value == observable_value)
        )

        query = _join_as_subquery(query, observable_value_query)

    if owner:
        owner_query = select(Alert).join(User, onclause=Alert.owner_uuid == User.uuid).where(User.username == owner)
        query = _join_as_subquery(query, owner_query)

    if queue:
        queue_query = select(Alert).join(Queue).where(Queue.value == queue)
        query = _join_as_subquery(query, queue_query)

    if tags:
        tag_filters = []
        for tag in tags.split(","):
            tag_filters.append(or_(Alert.tags.any(NodeTag.value == tag), Alert.child_tags.any(NodeTag.value == tag)))

        tags_query = select(Alert).where(and_(*tag_filters))
        query = _join_as_subquery(query, tags_query)

    if threat_actors:
        threat_actor_filters = []
        for threat_actor in threat_actors.split(","):
            threat_actor_filters.append(
                or_(
                    Alert.threat_actors.any(NodeThreatActor.value == threat_actor),
                    Alert.child_threat_actors.any(NodeThreatActor.value == threat_actor),
                )
            )
        threat_actor_query = select(Alert).where(and_(*threat_actor_filters))

        query = _join_as_subquery(query, threat_actor_query)

    if threats:
        threat_filters = []
        for threat in threats.split(","):
            threat_filters.append(
                or_(Alert.threats.any(NodeThreat.value == threat), Alert.child_threats.any(NodeThreat.value == threat))
            )
        threats_query = select(Alert).where(and_(*threat_filters))

        query = _join_as_subquery(query, threats_query)

    if tool:
        tool_query = select(Alert).join(AlertTool).where(AlertTool.value == tool)
        query = _join_as_subquery(query, tool_query)

    if tool_instance:
        tool_instance_query = select(Alert).join(AlertToolInstance).where(AlertToolInstance.value == tool_instance)
        query = _join_as_subquery(query, tool_instance_query)

    if type:
        type_query = select(Alert).join(AlertType).where(AlertType.value == type)
        query = _join_as_subquery(query, type_query)

    if sort:
        sort_split = sort.split("|")
        sort_by = sort_split[0]
        order = sort_split[1]

        # Only sort by disposition if we are not also filtering by disposition
        if sort_by.lower() == "disposition" and not disposition:
            if order == "asc":
                query = query.outerjoin(AlertDisposition).order_by(AlertDisposition.value.asc())
            else:
                query = query.outerjoin(AlertDisposition).order_by(AlertDisposition.value.desc())

        elif sort_by.lower() == "disposition_time":
            if order == "asc":
                query = query.order_by(Alert.disposition_time.asc())
            else:
                query = query.order_by(Alert.disposition_time.desc())

        # Only sort by disposition_user if we are not also filtering by disposition_user
        elif sort_by.lower() == "disposition_user" and not disposition_user:
            query = query.outerjoin(User, onclause=Alert.disposition_user_uuid == User.uuid).group_by(
                Alert.uuid, Node.uuid, User.username
            )
            if order == "asc":
                query = query.order_by(User.username.asc())
            else:
                query = query.order_by(User.username.desc())

        elif sort_by.lower() == "event_time":
            if order == "asc":
                query = query.order_by(Alert.event_time.asc())
            else:
                query = query.order_by(Alert.event_time.desc())

        elif sort_by.lower() == "insert_time":
            if order == "asc":
                query = query.order_by(Alert.insert_time.asc())
            else:
                query = query.order_by(Alert.insert_time.desc())

        elif sort_by.lower() == "name":
            if order == "asc":
                query = query.order_by(Alert.name.asc())
            else:
                query = query.order_by(Alert.name.desc())

        # Only sort by owner if we are not also filtering by owner
        elif sort_by.lower() == "owner" and not owner:
            query = query.outerjoin(User, onclause=Alert.owner_uuid == User.uuid).group_by(
                Alert.uuid, Node.uuid, User.username
            )
            if order == "asc":
                query = query.order_by(User.username.asc())
            else:
                query = query.order_by(User.username.desc())

        # Only sort by queue if we are not also filtering by queue
        elif sort_by.lower() == "queue" and not queue:
            if order == "asc":
                query = query.join(Queue).order_by(Queue.value.asc())
            else:
                query = query.join(Queue).order_by(Queue.value.desc())

        # Only sort by type if we are not also filtering by type
        elif sort_by.lower() == "type" and not type:
            if order == "asc":
                query = query.join(AlertType).order_by(AlertType.value.asc())
            else:
                query = query.join(AlertType).order_by(AlertType.value.desc())

    results = paginate(db, query)

    return results


def get_alert(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read_node_tree(root_node_uuid=uuid, db=db)


def get_alert_history(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read_history_records(history_table=AlertHistory, record_uuid=uuid, db=db)


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
    db: Session = Depends(get_db),
):
    for alert in alerts:
        # Update the Node attributes
        db_alert, diffs = update_node(node_update=alert, uuid=alert.uuid, db_table=Alert, db=db)

        # Get the data that was given in the request and use it to update the database object
        update_data = alert.dict(exclude_unset=True)

        if "description" in update_data:
            diffs.append(
                crud.create_diff(field="description", old=db_alert.description, new=update_data["description"])
            )
            db_alert.description = update_data["description"]

        if "disposition" in update_data:
            old = db_alert.disposition.value if db_alert.disposition else None
            diffs.append(crud.create_diff(field="disposition", old=old, new=update_data["disposition"]))

            db_alert.disposition = crud.read_by_value(
                value=update_data["disposition"], db_table=AlertDisposition, db=db
            )
            db_alert.disposition_time = datetime.utcnow()
            # db_alert.disposition_user = crud.read_user_by_username(username=claims["sub"], db=db)

        if "event_uuid" in update_data:
            diffs.append(crud.create_diff(field="event_uuid", old=db_alert.event_uuid, new=update_data["event_uuid"]))

            if update_data["event_uuid"]:
                db_alert.event = crud.read(uuid=update_data["event_uuid"], db_table=Event, db=db)

                # This counts as editing the event, so it should receive a new version.
                db_alert.event.version = uuid4()
            else:
                db_alert.event = None

        if "event_time" in update_data:
            diffs.append(crud.create_diff(field="event_time", old=db_alert.event_time, new=update_data["event_time"]))

            db_alert.event_time = update_data["event_time"]

        if "instructions" in update_data:
            diffs.append(
                crud.create_diff(field="instructions", old=db_alert.instructions, new=update_data["instructions"])
            )

            db_alert.instructions = update_data["instructions"]

        if "owner" in update_data:
            old = db_alert.owner.username if db_alert.owner else None
            diffs.append(crud.create_diff(field="owner", old=old, new=update_data["owner"]))

            db_alert.owner = crud.read_user_by_username(username=update_data["owner"], db=db)

        if "queue" in update_data:
            diffs.append(crud.create_diff(field="queue", old=db_alert.queue.value, new=update_data["queue"]))

            db_alert.queue = crud.read_by_value(value=update_data["queue"], db_table=Queue, db=db)

        crud.commit(db)

        response.headers["Content-Location"] = request.url_for("get_alert", uuid=alert.uuid)


helpers.api_route_update(router, update_alerts, path="/")


#
# DELETE
#


# We currently do not support deleting any Nodes.
