import json

from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from typing import Optional
from uuid import UUID, uuid4

from api_models.alert import AlertCreate, AlertTreeRead, AlertUpdate
from api_models.analysis import AnalysisNodeTreeRead
from api_models.observable import ObservableNodeTreeRead
from db import crud
from db.schemas.alert import Alert, AlertHistory
from db.schemas.alert_analysis_mapping import alert_analysis_mapping
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.alert_tool import AlertTool
from db.schemas.alert_tool_instance import AlertToolInstance
from db.schemas.alert_type import AlertType
from db.schemas.analysis_child_observable_mapping import analysis_child_observable_mapping
from db.schemas.event import Event
from db.schemas.node import Node
from db.schemas.node_tag import NodeTag
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_actor import NodeThreatActor
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType
from db.schemas.queue import Queue
from db.schemas.user import User


def build_read_all_query(
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
    observable: Optional[str] = None,  # Example: type|value
    observable_types: Optional[str] = None,
    observable_value: Optional[str] = None,
    owner: Optional[str] = None,
    queue: Optional[str] = None,
    sort: Optional[str] = None,  # Example: event_time|desc
    tags: Optional[str] = None,
    threat_actors: Optional[str] = None,
    threats: Optional[str] = None,
    tool: Optional[str] = None,
    tool_instance: Optional[str] = None,
) -> Select:
    def _join_as_subquery(query: Select, subquery: Select):
        s = subquery.subquery()
        return query.join(s, Alert.uuid == s.c.uuid).group_by(Alert.uuid, Node.uuid)

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
        observable_types_query = (
            select(Alert)
            .join(alert_analysis_mapping, onclause=alert_analysis_mapping.c.alert_uuid == Alert.uuid)
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid == alert_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .join(ObservableType)
            .where(ObservableType.value == observable_split[0], Observable.value == observable_split[1])
        )

        query = _join_as_subquery(query, observable_types_query)

    if observable_types:
        type_filters = [func.count(1).filter(ObservableType.value == t) > 0 for t in observable_types.split(",")]
        observable_types_query = (
            select(Alert)
            .join(alert_analysis_mapping, onclause=alert_analysis_mapping.c.alert_uuid == Alert.uuid)
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid == alert_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .join(ObservableType)
            .having(and_(*type_filters))
            .group_by(Alert.uuid, Node.uuid)
        )

        query = _join_as_subquery(query, observable_types_query)

    if observable_value:
        observable_value_query = (
            select(Alert)
            .join(alert_analysis_mapping, onclause=alert_analysis_mapping.c.alert_uuid == Alert.uuid)
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid == alert_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
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

    if alert_type:
        type_query = select(Alert).join(AlertType).where(AlertType.value == alert_type)
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
        elif sort_by.lower() == "type" and not alert_type:
            if order == "asc":
                query = query.join(AlertType).order_by(AlertType.value.asc())
            else:
                query = query.join(AlertType).order_by(AlertType.value.desc())

    return query


def create(model: AlertCreate, db: Session) -> Alert:
    # Create the new alert Node using the data from the request
    obj: Alert = crud.node.create(model=model, db_node_type=Alert, db=db, exclude={"history_username", "observables"})

    # Set the various alert properties
    obj.description = model.description
    obj.event_time = model.event_time
    obj.insert_time = model.insert_time
    obj.instructions = model.instructions
    obj.name = model.name
    obj.owner = crud.user.read_by_username(username=model.owner, db=db)
    obj.queue = crud.queue.read_by_value(value=model.queue, db=db)
    obj.root_analysis = crud.analysis.create_root(db=db)
    obj.tool = crud.alert_tool.read_by_value(value=model.tool, db=db)
    obj.tool_instance = crud.alert_tool_instance.read_by_value(value=model.tool_instance, db=db)
    obj.type = crud.alert_type.read_by_value(value=model.type, db=db)
    obj.uuid = model.uuid

    db.add(obj)
    db.flush()

    # Associate the root analysis with the submission
    crud.alert_analysis_mapping.create(analysis_uuid=obj.root_analysis_uuid, submission_uuid=obj.uuid, db=db)

    # Associate the root analysis with its observables
    obj.root_analysis.child_observables = [crud.observable.create(model=o, db=db) for o in model.observables]

    # Add an alert history entry if the history username was given. This would typically only be
    # supplied by the GUI when an analyst creates a manual alert.
    if model.history_username is not None:
        crud.history.record_node_create_history(
            record_node=obj,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            db=db,
        )

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> Optional[Alert]:
    return db.execute(select(Alert).where(Alert.uuid == uuid)).scalars().one_or_none()


def read_tree(uuid: UUID, db: Session) -> Optional[dict]:
    # The Alert db object has an "analyses" list that contains every analysis object regardless
    # of where it appears in the tree structure.
    db_alert = read_by_uuid(uuid=uuid, db=db)

    if db_alert is not None:
        # The analyses and observables need to be organized in a few dictionaries so that the tree
        # structure can be easily built:
        #
        # Dictionary of analysis objects where their UUID is the key
        # Dictionary of analysis objects where their target observable UUID is the key
        # Dictionary of observables where their UUID is the key
        analyses_by_target: dict[UUID, list[AnalysisNodeTreeRead]] = {}
        analyses_by_uuid: dict[UUID, AnalysisNodeTreeRead] = {}
        child_observables: dict[UUID, ObservableNodeTreeRead] = {}
        for db_analysis in db_alert.analyses:
            # Create an empty list if this target observable UUID has not been seen yet.
            if db_analysis.target_uuid not in analyses_by_target:
                analyses_by_target[db_analysis.target_uuid] = []

            # Add the analysis model to the two analysis dictionaries
            analysis = db_analysis.convert_to_pydantic()
            analyses_by_target[db_analysis.target_uuid].append(analysis)
            analyses_by_uuid[db_analysis.uuid] = analysis

            for db_child_observable in db_analysis.child_observables:
                # Add the observable model to the dictionary if it has not been seen yet.
                if db_child_observable.uuid not in child_observables:
                    child_observables[db_child_observable.uuid] = db_child_observable.convert_to_pydantic()

                # Add the observable as a child to the analysis model.
                analyses_by_uuid[db_analysis.uuid].children.append(child_observables[db_child_observable.uuid])

        # Loop over each overvable and add its analysis as a child
        for observable_uuid, observable in child_observables.items():

            if observable_uuid in analyses_by_target:
                observable.children = analyses_by_target[observable_uuid]

        # Create the AlertTree object and set its children to be the root analysis children.
        alert_tree = AlertTreeRead(**db_alert.__dict__)
        alert_tree.children = analyses_by_uuid[db_alert.root_analysis_uuid].children

        # Now that the tree structure is built, we need to walk it to mark which of the leaves have
        # already appeared in the tree. This is useful for when you might not want to display or
        # process a leaf in the tree if it is a duplicate (ex: the GUI auto-collapses duplicate leaves).
        #
        # But before the tree can be traversed, it needs to be serialized into JSON. If an observable or analysis
        # is repeated in the tree, it is just a reference to the same object, so updating its "first_appearance"
        # property would change the value for every instance of the object (which we do not want).
        #
        # Adapted from: https://www.geeksforgeeks.org/preorder-traversal-of-n-ary-tree-without-recursion/
        alert_tree_json: dict = json.loads(alert_tree.json(encoder=jsonable_encoder))
        unique_uuids: set[UUID] = set()
        unvisited = [alert_tree_json]
        while unvisited:
            current = unvisited.pop(0)

            if current["uuid"] in unique_uuids:
                current["first_appearance"] = False
            else:
                current["first_appearance"] = True
                unique_uuids.add(current["uuid"])

            for idx in range(len(current["children"]) - 1, -1, -1):
                unvisited.insert(0, current["children"][idx])

        return alert_tree_json

    return None


def update(model: AlertUpdate, db: Session):
    # Update the Node attributes
    alert, diffs = crud.node.update(model=model, uuid=model.uuid, db_table=Alert, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = model.dict(exclude_unset=True)

    if "description" in update_data:
        diffs.append(
            crud.history.create_diff(field="description", old=alert.description, new=update_data["description"])
        )
        alert.description = update_data["description"]

    if "disposition" in update_data and model.history_username:
        old_value = alert.disposition.value if alert.disposition else None
        diffs.append(crud.history.create_diff(field="disposition", old=old_value, new=update_data["disposition"]))
        alert.disposition = crud.alert_disposition.read_by_value(value=update_data["disposition"], db=db)
        alert.disposition_time = crud.helpers.utcnow()
        alert.disposition_user = crud.user.read_by_username(username=model.history_username, db=db)

    if "event_uuid" in update_data:
        diffs.append(crud.history.create_diff(field="event_uuid", old=alert.event_uuid, new=update_data["event_uuid"]))
        if update_data["event_uuid"]:
            alert.event = crud.event.read_by_uuid(uuid=update_data["event_uuid"], db=db)

            # This counts as editing the event, so it should receive a new version.
            alert.event.version = uuid4()
        else:
            alert.event = None

    if "event_time" in update_data:
        diffs.append(crud.history.create_diff(field="event_time", old=alert.event_time, new=update_data["event_time"]))
        alert.event_time = update_data["event_time"]

    if "instructions" in update_data:
        diffs.append(
            crud.history.create_diff(field="instructions", old=alert.instructions, new=update_data["instructions"])
        )
        alert.instructions = update_data["instructions"]

    if "owner" in update_data:
        old_value = alert.owner.username if alert.owner else None
        diffs.append(crud.history.create_diff(field="owner", old=old_value, new=update_data["owner"]))
        alert.owner = crud.user.read_by_username(username=update_data["owner"], db=db)

    if "queue" in update_data:
        diffs.append(crud.history.create_diff(field="queue", old=alert.queue.value, new=update_data["queue"]))
        alert.queue = crud.queue.read_by_value(value=update_data["queue"], db=db)

    # Add an alert history entry if the history username was given. This would typically only be
    # supplied by the GUI when an analyst updates an alert.
    if model.history_username is not None:
        crud.history.record_node_update_history(
            record_node=alert,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            diffs=diffs,
            db=db,
        )
