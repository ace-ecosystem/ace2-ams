import json
import uuid

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from typing import List, Optional, Union
from uuid import UUID

from api_models.alert import AlertCreate
from api_models.analysis import AnalysisCreate
from api_models.analysis_module_type import AnalysisModuleTypeCreate
from api_models.observable import ObservableCreate
from api_models.observable_type import ObservableTypeCreate
from core.auth import hash_password
from db import crud
from db.schemas.alert import Alert
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.alert_tool import AlertTool
from db.schemas.alert_tool_instance import AlertToolInstance
from db.schemas.alert_type import AlertType
from db.schemas.event import Event
from db.schemas.event_prevention_tool import EventPreventionTool
from db.schemas.event_remediation import EventRemediation
from db.schemas.event_risk_level import EventRiskLevel
from db.schemas.event_source import EventSource
from db.schemas.event_status import EventStatus
from db.schemas.event_type import EventType
from db.schemas.event_vector import EventVector
from db.schemas.node import Node
from db.schemas.node_comment import NodeComment
from db.schemas.node_detection_point import NodeDetectionPoint
from db.schemas.node_directive import NodeDirective
from db.schemas.node_relationship import NodeRelationship
from db.schemas.node_relationship_type import NodeRelationshipType
from db.schemas.node_tag import NodeTag
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_actor import NodeThreatActor
from db.schemas.node_threat_type import NodeThreatType
from db.schemas.node_tree import NodeTree
from db.schemas.observable import Observable
from db.schemas.queue import Queue
from db.schemas.user import User, UserHistory
from db.schemas.user_role import UserRole
from tests import factory


REALISTIC_ALERT_UUID = "02f8299b-2a24-400f-9751-7dd9164daf6a"


def _create_basic_object(value: str, db_table: DeclarativeMeta, db: Session):
    existing = crud.read_by_value(value=value, db_table=db_table, db=db, err_on_not_found=False)
    if existing:
        return existing

    obj = db_table(value=value)
    db.add(obj)
    crud.commit(db)
    return obj


def create_alert_disposition(value: str, db: Session, rank: Optional[int] = None) -> AlertDisposition:
    existing = crud.read_by_value(value=value, db_table=AlertDisposition, db=db, err_on_not_found=False)
    if existing:
        return existing

    if rank is None:
        existing_dispositions = crud.read_all(db_table=AlertDisposition, db=db)
        rank = len(existing_dispositions)

    disposition = AlertDisposition(value=value, rank=rank)
    db.add(disposition)
    crud.commit(db)
    return disposition


def create_alert_tool(value: str, db: Session) -> AlertTool:
    return _create_basic_object(db_table=AlertTool, value=value, db=db)


def create_alert_tool_instance(value: str, db: Session) -> AlertToolInstance:
    return _create_basic_object(db_table=AlertToolInstance, value=value, db=db)


def create_alert_type(value: str, db: Session) -> AlertType:
    return _create_basic_object(db_table=AlertType, value=value, db=db)


def create_event(
    name: str,
    db: Session,
    alert_time: Optional[datetime] = None,
    contain_time: Optional[datetime] = None,
    created_time: Optional[datetime] = None,
    disposition_time: Optional[datetime] = None,
    history_username: Optional[str] = None,
    owner: Optional[str] = None,
    prevention_tools: Optional[List[str]] = None,
    queue: str = "external",
    remediation_time: Optional[datetime] = None,
    remediations: Optional[List[str]] = None,
    risk_level: Optional[str] = None,
    source: Optional[str] = None,
    status: str = "OPEN",
    tags: Optional[List[str]] = None,
    threat_actors: Optional[List[str]] = None,
    threats: Optional[List[str]] = None,
    type: Optional[str] = None,
    vectors: Optional[List[str]] = None,
) -> Event:
    obj = Event(
        name=name,
        queue=create_queue(value=queue, db=db),
        status=create_event_status(value=status, db=db),
        uuid=uuid.uuid4(),
        version=uuid.uuid4(),
    )

    if alert_time:
        obj.alert_time = alert_time

    if contain_time:
        obj.contain_time = contain_time

    if created_time:
        obj.creation_time = created_time

    if disposition_time:
        obj.disposition_time = disposition_time

    if owner:
        obj.owner = create_user(email=f"{owner}@{owner}.com", username=owner, db=db, event_queue=queue)

    if prevention_tools:
        obj.prevention_tools = [create_event_prevention_tool(value=p, db=db) for p in prevention_tools]

    if remediation_time:
        obj.remediation_time = remediation_time

    if remediations:
        obj.remediations = [create_event_remediation(value=r, db=db) for r in remediations]

    if risk_level:
        obj.risk_level = create_event_risk_level(value=risk_level, db=db)

    if source:
        obj.source = create_event_source(value=source, db=db)

    if tags:
        obj.tags = [create_node_tag(value=tag, db=db) for tag in tags]

    if threat_actors:
        obj.threat_actors = [create_node_threat_actor(value=threat_actor, db=db) for threat_actor in threat_actors]

    if threats:
        obj.threats = [create_node_threat(value=threat, db=db) for threat in threats]

    if type:
        obj.type = create_event_type(value=type, db=db)

    if vectors:
        obj.vectors = [create_event_vector(value=v, db=db) for v in vectors]

    db.add(obj)
    crud.commit(db)

    if history_username:
        crud.record_node_create_history(
            record_node=obj,
            action_by=create_user(username=history_username, db=db),
            db=db,
        )

    return obj


def create_event_prevention_tool(value: str, db: Session, queues: List[str] = None) -> EventPreventionTool:
    if queues is None:
        queues = ["external"]

    obj: EventPreventionTool = _create_basic_object(db_table=EventPreventionTool, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_event_remediation(value: str, db: Session, queues: List[str] = None) -> EventRemediation:
    if queues is None:
        queues = ["external"]

    obj: EventRemediation = _create_basic_object(db_table=EventRemediation, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_event_risk_level(value: str, db: Session, queues: List[str] = None) -> EventRiskLevel:
    if queues is None:
        queues = ["external"]

    obj: EventRiskLevel = _create_basic_object(db_table=EventRiskLevel, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_event_source(value: str, db: Session, queues: List[str] = None) -> EventSource:
    if queues is None:
        queues = ["external"]

    obj: EventSource = _create_basic_object(db_table=EventSource, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_event_status(value: str, db: Session, queues: List[str] = None) -> EventStatus:
    if queues is None:
        queues = ["external"]

    obj: EventStatus = _create_basic_object(db_table=EventStatus, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_event_type(value: str, db: Session, queues: List[str] = None) -> EventType:
    if queues is None:
        queues = ["external"]

    obj: EventType = _create_basic_object(db_table=EventType, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_event_vector(value: str, db: Session, queues: List[str] = None) -> EventVector:
    if queues is None:
        queues = ["external"]

    obj: EventVector = _create_basic_object(db_table=EventVector, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_node_comment(
    node: Node,
    username: str,
    value: str,
    db: Session,
    history_username: Optional[str] = None,
    insert_time: Optional[datetime] = None,
) -> NodeComment:
    if insert_time is None:
        insert_time = crud.helpers.utcnow()

    user = create_user(username=username, db=db)

    obj = NodeComment(insert_time=insert_time, node_uuid=node.uuid, user=user, uuid=uuid.uuid4(), value=value)
    db.add(obj)
    crud.commit(db)

    if history_username:
        crud.record_node_update_history(
            record_node=node,
            action_by=create_user(username=history_username, display_name=history_username, db=db),
            action_time=insert_time,
            diffs=[crud.Diff(field="comments", added_to_list=[obj.value], removed_from_list=[])],
            db=db,
        )

    return obj


def create_node_detection_point(
    node: Node,
    value: str,
    db: Session,
    history_username: Optional[str] = None,
    insert_time: Optional[datetime] = None,
) -> NodeDetectionPoint:
    if insert_time is None:
        insert_time = crud.helpers.utcnow()

    obj = NodeDetectionPoint(insert_time=insert_time, node_uuid=node.uuid, uuid=uuid.uuid4(), value=value)
    db.add(obj)
    crud.commit(db)

    if history_username:
        crud.record_node_update_history(
            record_node=node,
            action_by=create_user(username=history_username, display_name=history_username, db=db),
            action_time=insert_time,
            diffs=[crud.Diff(field="detection_points", added_to_list=[obj.value], removed_from_list=[])],
            db=db,
        )

    return obj


def create_node_directive(value: str, db: Session) -> NodeDirective:
    return _create_basic_object(db_table=NodeDirective, value=value, db=db)


def create_node_relationship(node: Node, related_node: Node, type: str, db: Session) -> NodeRelationship:
    obj = NodeRelationship(
        node_uuid=node.uuid, related_node=related_node, type=create_node_relationship_type(value=type, db=db)
    )
    db.add(obj)
    crud.commit(db)
    return obj


def create_node_relationship_type(value: str, db: Session) -> NodeRelationshipType:
    return _create_basic_object(db_table=NodeRelationshipType, value=value, db=db)


def create_node_tag(value: str, db: Session) -> NodeTag:
    return _create_basic_object(db_table=NodeTag, value=value, db=db)


def create_node_threat_actor(value: str, db: Session, queues: List[str] = None) -> NodeThreatActor:
    if queues is None:
        queues = ["external"]

    obj: NodeThreatActor = _create_basic_object(db_table=NodeThreatActor, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_node_threat_type(value: str, db: Session, queues: List[str] = None) -> NodeThreatType:
    if queues is None:
        queues = ["external"]

    obj: NodeThreatType = _create_basic_object(db_table=NodeThreatType, value=value, db=db)
    obj.queues = [create_queue(value=queue, db=db) for queue in queues]

    return obj


def create_queue(value: str, db: Session) -> Queue:
    return _create_basic_object(db_table=Queue, value=value, db=db)


def create_user_role(value: str, db: Session) -> UserRole:
    return _create_basic_object(db_table=UserRole, value=value, db=db)


def create_alert_from_json_file(db: Session, json_path: str, alert_name: str) -> Alert:
    def _create_analysis(a, root_analysis_uuid: UUID, parent_observable: Observable):
        if "observables" in a:
            for observable in a["observables"]:
                crud.observable_type.create(model=ObservableTypeCreate(value=observable["type"]), db=db)

        analysis_module_type = crud.analysis_module_type.create(model=AnalysisModuleTypeCreate(value=a["type"]), db=db)
        analysis = crud.analysis.create(
            model=AnalysisCreate(
                analysis_module_type_uuid=analysis_module_type.uuid,
                child_observables=a["observables"] if "observables" in a else [],
                details=json.dumps(a["details"]) if "details" in a else None,
                parent_observable_uuid=parent_observable.uuid,
                root_analysis_uuid=root_analysis_uuid,
                run_time=crud.helpers.utcnow(),
            ),
            db=db,
        )

        if "observables" in a:
            for observable in a["observables"]:
                analysis.child_observables.append(
                    _create_observable(o=observable, root_analysis_uuid=root_analysis_uuid)
                )

        return analysis

    def _create_observable(o, root_analysis_uuid: UUID) -> ObservableCreate:
        # crud.observable_type.create(model=ObservableTypeCreate(value=o["type"]), db=db)
        # observable = crud.observable.create(model=ObservableCreate(**o), db=db)

        # if "analyses" in o:
        #     for analysis in o["analyses"]:
        #         _create_analysis(a=analysis, root_analysis_uuid=root_analysis_uuid, parent_observable=observable)

        # return observable

        crud.observable_type.create(model=ObservableTypeCreate(value=o["type"]), db=db)
        observable = ObservableCreate(
            for_detection=o["for_detection"] if "for_detection" in o else False,
            tags=o["tags"] if "tags" in o else [],
            type=o["type"],
            value=o["value"],
        )
        if "analyses" in o:
            for a in o["analyses"]:
                analysis_module_type = crud.analysis_module_type.create(
                    AnalysisModuleTypeCreate(value=a["type"]), db=db
                )
                observable.analyses.append(
                    AnalysisCreate(
                        analysis_module_type_uuid=analysis_module_type.uuid,
                        child_observables=[
                            _create_observable(o=co, root_analysis_uuid=root_analysis_uuid) for co in a["observables"]
                        ]
                        if "observables" in a
                        else [],
                        details=json.dumps(a["details"]) if "details" in a else None,
                        parent_observable_uuid=observable.uuid,
                        root_analysis_uuid=root_analysis_uuid,
                        run_time=crud.helpers.utcnow(),
                    )
                )

        return observable

    def _replace_tokens(text: str, token: str, base_replacement_string: str) -> str:
        for i in range(text.count(token)):
            text = text.replace(token, f"{base_replacement_string}{i}", 1)

        return text

    with open(json_path) as f:
        text = f.read()

        text = text.replace("<ALERT_NAME>", alert_name)
        text = _replace_tokens(text, "<A_TYPE>", "a_type")
        text = _replace_tokens(text, "<O_TYPE>", "o_type")
        text = _replace_tokens(text, "<O_VALUE>", "o_value")
        text = _replace_tokens(text, "<TAG>", "tag")

        data = json.loads(text)

    if "alert_uuid" in data:
        alert_uuid = data["alert_uuid"]
        existing_alert = crud.alert.read_by_uuid(uuid=alert_uuid, db=db)
        if existing_alert is not None:
            return existing_alert
    else:
        alert_uuid = uuid.uuid4()

    disposition_user = None
    if "disposition_user" in data:
        disposition_user = data["disposition_user"]

    name = "Test Alert"
    if "name" in data:
        name = data["name"]

    owner = None
    if "owner" in data:
        owner = data["owner"]

    # # Build the ObservableCreate and AnalysisCreate objects for the observables
    # observables: list[ObservableCreate] = []
    # for o in data["observables"]:
    #     observable = ObservableCreate(
    #         for_detection=o["for_detection"] if "for_detection" in o else False,
    #         tags=o["tags"] if "tags" in o else [],
    #         type=o["type"],
    #         value=o["value"],
    #     )
    #     if "analyses" in o:
    #         for a in o["analyses"]:
    #             analysis_module_type = crud.analysis_module_type.create(
    #                 AnalysisModuleTypeCreate(value=a["type"]), db=db
    #             )
    #             observable.analyses.append(
    #                 AnalysisCreate(
    #                     analysis_module_type_uuid=analysis_module_type.uuid,
    #                     details=json.dumps(a["details"]) if "details" in a else None,
    #                     parent_observable_uuid=observable.uuid,
    #                     root_analysis_uuid=alert_uuid,
    #                     run_time=crud.helpers.utcnow(),
    #                 )
    #             )
    #     observables.append(observable)

    alert = factory.alert.create(
        db=db,
        alert_uuid=alert_uuid,
        name=name,
        observables=[_create_observable(o=o, root_analysis_uuid=alert_uuid) for o in data["observables"]],
        owner=owner,
        updated_by_user=disposition_user,
    )

    # for o in data["observables"]:
    #     _create_observable(o=o, root_analysis_uuid=alert.uuid)

    return alert


def read_node_tree_leaf(root_node_uuid: UUID, node_uuid: UUID, db: Session) -> Optional[NodeTree]:
    return (
        db.execute(select(NodeTree).where(NodeTree.root_node_uuid == root_node_uuid, NodeTree.node_uuid == node_uuid))
        .scalars()
        .one_or_none()
    )


def stringify_alert_tree(alert_tree: dict):
    def _stringify_children(children: list[dict], depth=0, string=""):
        for child in children:
            duplicate = "" if child["first_appearance"] else " (Duplicate)"
            if child["node_type"] == "observable":
                string += f"{' '*depth}{child['type']['value']}: {child['value']}{duplicate}\n"
                if child["children"]:
                    string = _stringify_children(children=child["children"], depth=depth + 2, string=string)
            if child["node_type"] == "analysis":
                string += f"{' '*depth}{child['analysis_module_type']['value']}{duplicate}\n"
                if child["children"]:
                    string = _stringify_children(children=child["children"], depth=depth + 2, string=string)

        return string

    return _stringify_children(children=alert_tree["children"])
