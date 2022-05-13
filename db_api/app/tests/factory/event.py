from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional

from api_models.event import EventCreate
from api_models.node_tag import NodeTagCreate
from api_models.queue import QueueCreate
from db import crud
from tests import factory


def create(
    name: str,
    db: Session,
    alert_time: Optional[datetime] = None,
    contain_time: Optional[datetime] = None,
    created_time: Optional[datetime] = None,
    disposition_time: Optional[datetime] = None,
    event_queue: str = "external",
    event_type: Optional[str] = None,
    history_username: Optional[str] = None,
    owner: Optional[str] = None,
    prevention_tools: Optional[list[str]] = None,
    remediation_time: Optional[datetime] = None,
    remediations: Optional[list[str]] = None,
    risk_level: Optional[str] = None,
    source: Optional[str] = None,
    status: str = "OPEN",
    tags: Optional[list[str]] = None,
    threat_actors: Optional[list[str]] = None,
    threats: Optional[list[str]] = None,
    vectors: Optional[list[str]] = None,
):
    # Set default values
    if prevention_tools is None:
        prevention_tools = []

    if remediations is None:
        remediations = []

    if tags is None:
        tags = []

    if threat_actors is None:
        threat_actors = []

    if threats is None:
        threats = []

    if vectors is None:
        vectors = []

    # Create the objects the event will need
    crud.queue.create_or_read(model=QueueCreate(value=event_queue), db=db)

    if event_type:
        factory.event_type.create(value=event_type, queues=[event_queue], db=db)

    if owner:
        factory.user.create(username=owner, event_queue=event_queue, db=db)

    for p in prevention_tools:
        factory.event_prevention_tool.create(value=p, queues=[event_queue], db=db)

    for r in remediations:
        factory.event_remediation.create(value=r, queues=[event_queue], db=db)

    if risk_level:
        factory.event_risk_level.create(value=risk_level, queues=[event_queue], db=db)

    if source:
        factory.event_source.create(value=source, queues=[event_queue], db=db)

    factory.event_status.create(value=status, queues=[event_queue], db=db)

    for t in tags:
        crud.node_tag.create_or_read(model=NodeTagCreate(value=t), db=db)

    for t in threat_actors:
        factory.node_threat_actor.create(value=t, queues=[event_queue], db=db)

    for t in threats:
        factory.node_threat.create(value=t, queues=[event_queue], db=db)

    for v in vectors:
        factory.event_vector.create(value=v, queues=[event_queue], db=db)

    return crud.event.create(
        model=EventCreate(
            alert_time=alert_time,
            contain_time=contain_time,
            created_time=created_time,
            disposition_time=disposition_time,
            history_username=history_username,
            name=name,
            owner=owner,
            prevention_tools=prevention_tools,
            queue=event_queue,
            remediation_time=remediation_time,
            remediations=remediations,
            risk_level=risk_level,
            source=source,
            status=status,
            tags=tags,
            threat_actors=threat_actors,
            threats=threats,
            type=event_type,
            vectors=vectors,
        ),
        db=db,
    )
