import uuid

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from typing import List, Optional

from core.auth import hash_password
from db import crud
from db.schemas.alert import Alert
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.alert_queue import AlertQueue
from db.schemas.alert_tool import AlertTool
from db.schemas.alert_tool_instance import AlertToolInstance
from db.schemas.alert_type import AlertType
from db.schemas.analysis import Analysis
from db.schemas.event import Event
from db.schemas.event_status import EventStatus
from db.schemas.node_directive import NodeDirective
from db.schemas.node_tag import NodeTag
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_actor import NodeThreatActor
from db.schemas.node_threat_type import NodeThreatType
from db.schemas.observable_type import ObservableType
from db.schemas.user import User
from db.schemas.user_role import UserRole


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


def create_alert_queue(value: str, db: Session) -> AlertQueue:
    return _create_basic_object(db_table=AlertQueue, value=value, db=db)


def create_alert_tool(value: str, db: Session) -> AlertTool:
    return _create_basic_object(db_table=AlertTool, value=value, db=db)


def create_alert_tool_instance(value: str, db: Session) -> AlertToolInstance:
    return _create_basic_object(db_table=AlertToolInstance, value=value, db=db)


def create_alert_type(value: str, db: Session) -> AlertType:
    return _create_basic_object(db_table=AlertType, value=value, db=db)


def create_alert(
    db: Session,
    alert_queue: str = "test_queue",
    alert_type: str = "test_type",
    disposition: Optional[str] = None,
    disposition_time: Optional[datetime] = None,
    disposition_user: Optional[str] = None,
    event_time: datetime = None,
    insert_time: datetime = None,
    name: str = "Test Alert",
    owner: Optional[str] = None,
    tool: str = "test_tool",
    tool_instance: str = "test_tool_instance",
) -> Alert:
    """
    Helper function to create an alert. Returns a tuple of (alert_uuid, analysis_uuid)
    """

    if event_time is None:
        event_time = datetime.utcnow()

    if insert_time is None:
        insert_time = datetime.utcnow()

    alert = Alert(
        analysis=Analysis(version=uuid.uuid4()),
        event_time=event_time,
        insert_time=insert_time,
        name=name,
        queue=create_alert_queue(value=alert_queue, db=db),
        tool=create_alert_tool(value=tool, db=db),
        tool_instance=create_alert_tool_instance(value=tool_instance, db=db),
        type=create_alert_type(value=alert_type, db=db),
        uuid=uuid.uuid4(),
        version=uuid.uuid4(),
    )

    if disposition:
        alert.disposition = create_alert_disposition(value=disposition, db=db)

    if disposition_time:
        alert.disposition_time = disposition_time

    if disposition_user:
        alert.disposition_user = create_user(username=disposition_user, db=db, alert_queue=alert_queue)

    if event_time:
        alert.event_time = event_time

    if insert_time:
        alert.insert_time = insert_time

    if owner:
        alert.owner = create_user(username=owner, db=db, alert_queue=alert_queue)

    db.add(alert)
    crud.commit(db)

    return alert


def create_analysis(db: Session) -> Analysis:
    obj = Analysis(version=uuid.uuid4())
    db.add(obj)
    return obj


def create_event(name: str, db: Session) -> Event:
    """
    Helper function to create an event. Returns the event.
    """

    obj = Event(name=name, uuid=uuid.uuid4(), version=uuid.uuid4())
    db.add(obj)
    return obj


def create_event_status(value: str, db: Session) -> EventStatus:
    return _create_basic_object(db_table=EventStatus, value=value, db=db)


def create_node_directive(value: str, db: Session) -> NodeDirective:
    return _create_basic_object(db_table=NodeDirective, value=value, db=db)


def create_node_tag(value: str, db: Session) -> NodeTag:
    return _create_basic_object(db_table=NodeTag, value=value, db=db)


def create_node_threat_actor(value: str, db: Session) -> NodeThreatActor:
    return _create_basic_object(db_table=NodeThreatActor, value=value, db=db)


def create_node_threat(value: str, db: Session, types: List[str] = None) -> NodeThreat:
    existing = crud.read_by_value(value=value, db_table=NodeThreat, db=db, err_on_not_found=False)
    if existing:
        return existing

    if types is None:
        types = ["test_type"]

    obj = NodeThreat(value=value, types=[create_node_threat_type(value=t, db=db) for t in types])
    db.add(obj)
    return obj


def create_node_threat_type(value: str, db: Session) -> NodeThreatType:
    return _create_basic_object(db_table=NodeThreatType, value=value, db=db)


def create_observable_type(value: str, db: Session) -> ObservableType:
    return _create_basic_object(db_table=ObservableType, value=value, db=db)


def create_user(
    username: str,
    db: Session,
    alert_queue: str = "test_queue",
    display_name: str = "Analyst",
    email: Optional[str] = None,
    password: str = "asdfasdf",
    roles: List[str] = None,
) -> User:
    existing = crud.read_user_by_username(username=username, db=db, err_on_not_found=False)
    if existing:
        return existing

    if email is None:
        email = f"{username}@test.com"

    if roles is None:
        roles = [create_user_role(value="test_role", db=db)]
    else:
        roles = [create_user_role(value=r, db=db) for r in roles]

    obj = User(
        default_alert_queue=create_alert_queue(value=alert_queue, db=db),
        display_name=display_name,
        email=email,
        password=hash_password(password),
        roles=roles,
        username=username,
    )
    db.add(obj)
    return obj


def create_user_role(value: str, db: Session) -> UserRole:
    return _create_basic_object(db_table=UserRole, value=value, db=db)
