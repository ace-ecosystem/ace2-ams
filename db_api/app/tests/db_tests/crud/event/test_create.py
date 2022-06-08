from datetime import timedelta
from uuid import uuid4

from api_models.event import EventCreate
from db import crud
from tests import factory


def test_create(db):
    # Create the various objects to link to the event
    factory.event_prevention_tool.create_or_read(value="tool", db=db)
    factory.event_remediation.create_or_read(value="remediation", db=db)
    factory.event_risk_level.create_or_read(value="1", db=db)
    factory.event_source.create_or_read(value="email", db=db)
    factory.event_status.create_or_read(value="OPEN", db=db)
    factory.event_type.create_or_read(value="phish", db=db)
    factory.event_vector.create_or_read(value="email", db=db)
    factory.tag.create_or_read(value="tag", db=db)
    factory.node_threat.create_or_read(value="threat", db=db)
    factory.node_threat_actor.create_or_read(value="actor", db=db)

    # Create the event
    now = crud.helpers.utcnow()
    event = crud.event.create_or_read(
        model=EventCreate(
            alert_time=now,
            contain_time=now,
            created_time=now,
            disposition_time=now,
            event_time=now,
            history_username="analyst",
            name="test event",
            owner="analyst",
            ownership_time=now,
            prevention_tools=["tool"],
            queue="external",
            remediation_time=now,
            remediations=["remediation"],
            risk_level="1",
            source="email",
            status="OPEN",
            tags=["tag"],
            threat_actors=["actor"],
            threats=["threat"],
            type="phish",
            vectors=["email"],
        ),
        db=db,
    )

    assert event.alert_time == now
    assert event.alert_uuids == []
    assert event.alerts == []
    assert event.auto_alert_time is None
    assert event.auto_disposition_time is None
    assert event.auto_event_time is None
    assert event.auto_ownership_time is None
    assert event.contain_time == now
    assert event.created_time == now
    assert event.disposition is None
    assert event.disposition_time == now
    assert event.event_time == now
    assert event.name == "test event"
    assert event.owner.username == "analyst"
    assert event.ownership_time == now
    assert event.prevention_tools[0].value == "tool"
    assert event.queue.value == "external"
    assert event.remediation_time == now
    assert event.remediations[0].value == "remediation"
    assert event.risk_level.value == "1"
    assert event.source.value == "email"
    assert event.status.value == "OPEN"
    assert event.tags[0].value == "tag"
    assert event.threat_actors[0].value == "actor"
    assert event.threats[0].value == "threat"
    assert event.type.value == "phish"
    assert event.vectors[0].value == "email"

    # Add an alert to the event
    alert = factory.submission.create(
        alert=True,
        disposition="DELIVERY",
        event=event,
        event_time=now - timedelta(seconds=30),
        history_username="analyst",
        insert_time=now - timedelta(seconds=30),
        owner="analyst",
        update_time=now - timedelta(seconds=30),
        updated_by_user="analyst",
        db=db,
    )

    assert event.alert_uuids == [alert.uuid]
    assert event.alerts == [alert]
    assert event.auto_alert_time == alert.insert_time
    assert event.auto_disposition_time == alert.disposition_time_earliest
    assert event.auto_event_time == alert.event_time
    assert event.auto_ownership_time == alert.ownership_time_earliest
    assert event.disposition.value == "DELIVERY"
    assert event.disposition_time == now

    # There should be a history entry for creating the event
    assert len(event.history) == 1
    assert event.history[0].action == "CREATE"


def test_create_duplicate_uuid(db):
    obj1 = factory.event.create_or_read(name="test event", uuid=uuid4(), db=db)

    # Trying to create an event using an existing UUID should return the existing event
    obj2 = factory.event.create_or_read(name="new event", uuid=obj1.uuid, db=db)
    assert obj2 == obj1
