from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID, uuid4

from api_models.event import EventCreate
from db import crud
from tests import factory


def create_or_read(
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
    severity: Optional[str] = None,
    source: Optional[str] = None,
    status: str = "OPEN",
    tags: Optional[list[str]] = None,
    threat_actors: Optional[list[str]] = None,
    threats: Optional[list[str]] = None,
    uuid: Optional[UUID] = None,
    vectors: Optional[list[str]] = None,
):
    # Set default values
    if created_time is None:
        created_time = crud.helpers.utcnow()

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

    if uuid is None:
        uuid = uuid4()

    if vectors is None:
        vectors = []

    # Create the objects the event will need
    factory.queue.create_or_read(value=event_queue, db=db)

    if event_type:
        factory.event_type.create_or_read(value=event_type, queues=[event_queue], db=db)

    if owner:
        factory.user.create_or_read(username=owner, event_queue=event_queue, db=db)

    for p in prevention_tools:
        factory.event_prevention_tool.create_or_read(value=p, queues=[event_queue], db=db)

    for r in remediations:
        factory.event_remediation.create_or_read(value=r, queues=[event_queue], db=db)

    if severity:
        factory.event_severity.create_or_read(value=severity, queues=[event_queue], db=db)

    if source:
        factory.event_source.create_or_read(value=source, queues=[event_queue], db=db)

    factory.event_status.create_or_read(value=status, queues=[event_queue], db=db)

    for t in tags:
        factory.metadata_tag.create_or_read(value=t, db=db)

    for t in threat_actors:
        factory.node_threat_actor.create_or_read(value=t, queues=[event_queue], db=db)

    for t in threats:
        factory.node_threat.create_or_read(value=t, queues=[event_queue], db=db)

    for v in vectors:
        factory.event_vector.create_or_read(value=v, queues=[event_queue], db=db)

    obj = crud.event.create_or_read(
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
            severity=severity,
            source=source,
            status=status,
            tags=tags,
            threat_actors=threat_actors,
            threats=threats,
            type=event_type,
            uuid=uuid,
            vectors=vectors,
        ),
        db=db,
    )

    db.commit()

    return obj
