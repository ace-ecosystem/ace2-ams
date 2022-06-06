import json

from datetime import timedelta

from api_models.analysis_details import (
    SandboxAnalysisDetails,
    SandboxContactedHost,
    SandboxDnsRequest,
    SandboxDroppedFile,
    SandboxHttpRequest,
    SandboxProcess,
)
from api_models.event_summaries import URLDomainSummary
from db import crud
from tests import factory


def test_filter_by_alert_time_after_alert_insert_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(event=event1, insert_time=now - timedelta(seconds=5), db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(event=event2, insert_time=now, db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    factory.submission.create(event=event3, insert_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(alert_time_after=now, db=db)
    assert result == [event3]


def test_filter_by_alert_time_before_alert_insert_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(event=event1, insert_time=now - timedelta(seconds=5), db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(event=event2, insert_time=now, db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    factory.submission.create(event=event3, insert_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(alert_time_before=now, db=db)
    assert result == [event1]


def test_filter_by_alert_time_after_event_alert_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", alert_time=now - timedelta(seconds=5), db=db)
    factory.submission.create(event=event1, insert_time=now - timedelta(days=1), db=db)

    event2 = factory.event.create_or_read(name="event2", alert_time=now, db=db)
    factory.submission.create(event=event2, insert_time=now - timedelta(days=1), db=db)

    event3 = factory.event.create_or_read(name="event3", alert_time=now + timedelta(seconds=5), db=db)
    factory.submission.create(event=event3, insert_time=now - timedelta(days=1), db=db)

    result = crud.event.read_all(alert_time_after=now, db=db)
    assert result == [event3]


def test_filter_by_alert_time_before_event_alert_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", alert_time=now - timedelta(seconds=5), db=db)
    factory.submission.create(event=event1, db=db)

    event2 = factory.event.create_or_read(name="event2", alert_time=now, db=db)
    factory.submission.create(event=event2, db=db)

    event3 = factory.event.create_or_read(name="event3", alert_time=now + timedelta(seconds=5), db=db)
    factory.submission.create(event=event3, db=db)

    result = crud.event.read_all(alert_time_before=now, db=db)
    assert result == [event1]


def test_filter_by_contain_time_after(db):
    now = crud.helpers.utcnow()

    factory.event.create_or_read(name="event1", contain_time=now - timedelta(seconds=5), db=db)
    factory.event.create_or_read(name="event2", contain_time=now, db=db)
    event3 = factory.event.create_or_read(name="event3", contain_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(contain_time_after=now, db=db)
    assert result == [event3]


def test_filter_by_contain_time_before(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", contain_time=now - timedelta(seconds=5), db=db)
    factory.event.create_or_read(name="event2", contain_time=now, db=db)
    factory.event.create_or_read(name="event3", contain_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(contain_time_before=now, db=db)
    assert result == [event1]


def test_filter_by_created_time_after(db):
    now = crud.helpers.utcnow()

    factory.event.create_or_read(name="event1", created_time=now - timedelta(seconds=5), db=db)
    factory.event.create_or_read(name="event2", created_time=now, db=db)
    event3 = factory.event.create_or_read(name="event3", created_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(created_time_after=now, db=db)
    assert result == [event3]


def test_filter_by_created_time_before(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", created_time=now - timedelta(seconds=5), db=db)
    factory.event.create_or_read(name="event2", created_time=now, db=db)
    factory.event.create_or_read(name="event3", created_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(created_time_before=now, db=db)
    assert result == [event1]


def test_filter_by_disposition(db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(event=event1, db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(event=event2, disposition="RECONNAISSANCE", db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    factory.submission.create(event=event3, disposition="DELIVERY", db=db)

    result = crud.event.read_all(disposition="DELIVERY", db=db)
    assert result == [event3]

    result = crud.event.read_all(disposition="none", db=db)
    assert result == [event1]


def test_filter_by_disposition_time_after_event_disposition_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", disposition_time=now - timedelta(seconds=5), db=db)
    factory.submission.create(event=event1, db=db)

    event2 = factory.event.create_or_read(name="event2", disposition_time=now, db=db)
    factory.submission.create(event=event2, db=db)

    event3 = factory.event.create_or_read(name="event3", disposition_time=now + timedelta(seconds=5), db=db)
    factory.submission.create(event=event3, db=db)

    result = crud.event.read_all(disposition_time_after=now, db=db)
    assert result == [event3]


def test_filter_by_disposition_time_before_event_disposition_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", disposition_time=now - timedelta(seconds=5), db=db)
    factory.submission.create(event=event1, db=db)

    event2 = factory.event.create_or_read(name="event2", disposition_time=now, db=db)
    factory.submission.create(event=event2, db=db)

    event3 = factory.event.create_or_read(name="event3", disposition_time=now + timedelta(seconds=5), db=db)
    factory.submission.create(event=event3, db=db)

    result = crud.event.read_all(disposition_time_before=now, db=db)
    assert result == [event1]


def test_filter_by_disposition_time_after_alert_disposition_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(
        event=event1,
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now - timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(
        event=event2,
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now,
        history_username="analyst",
        db=db,
    )

    event3 = factory.event.create_or_read(name="event3", db=db)
    factory.submission.create(
        event=event3,
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now + timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )

    result = crud.event.read_all(disposition_time_after=now, db=db)
    assert result == [event3]


def test_filter_by_disposition_time_before_alert_disposition_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(
        event=event1,
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now - timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(
        event=event2,
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now,
        history_username="analyst",
        db=db,
    )

    event3 = factory.event.create_or_read(name="event3", db=db)
    factory.submission.create(
        event=event3,
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now + timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )

    result = crud.event.read_all(disposition_time_before=now, db=db)
    assert result == [event1]


def test_filter_by_event_type(db):
    factory.event.create_or_read(name="event1", event_type="type1", db=db)
    factory.event.create_or_read(name="event2", event_type="type2", db=db)
    event3 = factory.event.create_or_read(name="event3", event_type="type3", db=db)

    result = crud.event.read_all(event_type="type3", db=db)
    assert result == [event3]


def test_filter_by_name(db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    event2 = factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", db=db)

    result = crud.event.read_all(name="event3", db=db)
    assert result == [event3]

    result = crud.event.read_all(name="event", db=db)
    assert result == [event1, event2, event3]


def test_filter_by_observable(db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(event=event2, db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(event=event3, db=db)
    factory.observable.create_or_read(type="type3", value="value3", parent_analysis=alert3.root_analysis, db=db)

    result = crud.event.read_all(observable="type3|value3", db=db)
    assert result == [event3]


def test_filter_by_observable_types(db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(event=event2, db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(event=event3, db=db)
    factory.observable.create_or_read(type="type3", value="value3", parent_analysis=alert3.root_analysis, db=db)

    result = crud.event.read_all(observable_types="type3", db=db)
    assert result == [event3]


def test_filter_by_observable_value(db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(event=event2, db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(event=event3, db=db)
    factory.observable.create_or_read(type="type3", value="value3", parent_analysis=alert3.root_analysis, db=db)

    result = crud.event.read_all(observable_value="value3", db=db)
    assert result == [event3]


def test_filter_by_owner(db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", owner="analyst", db=db)

    result = crud.event.read_all(owner="analyst", db=db)
    assert result == [event3]


def test_filter_by_prevention_tools(db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", prevention_tools=["tool3"], db=db)

    result = crud.event.read_all(prevention_tools="tool3", db=db)
    assert result == [event3]


def test_filter_by_queue(db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", event_queue="queue3", db=db)

    result = crud.event.read_all(queue="queue3", db=db)
    assert result == [event3]


def test_filter_by_remediation_time_after(db):
    now = crud.helpers.utcnow()

    factory.event.create_or_read(name="event1", remediation_time=now - timedelta(seconds=5), db=db)
    factory.event.create_or_read(name="event2", remediation_time=now, db=db)
    event3 = factory.event.create_or_read(name="event3", remediation_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(remediation_time_after=now, db=db)
    assert result == [event3]


def test_filter_by_remediation_time_before(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", remediation_time=now - timedelta(seconds=5), db=db)
    factory.event.create_or_read(name="event2", remediation_time=now, db=db)
    factory.event.create_or_read(name="event3", remediation_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(remediation_time_before=now, db=db)
    assert result == [event1]


def test_filter_by_remediations(db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", remediations=["remediation3"], db=db)

    result = crud.event.read_all(remediations="remediation3", db=db)
    assert result == [event3]


def test_filter_by_risk_level(db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", risk_level="level3", db=db)

    result = crud.event.read_all(risk_level="level3", db=db)
    assert result == [event3]


def test_filter_by_source(db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", source="source3", db=db)

    result = crud.event.read_all(source="source3", db=db)
    assert result == [event3]


def test_filter_by_status(db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", status="status3", db=db)

    result = crud.event.read_all(status="status3", db=db)
    assert result == [event3]


def test_filter_by_tags(db):
    event1 = factory.event.create_or_read(name="event1", tags=["event1_tag"], db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(event=event2, tags=["alert2_tag"], db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(event=event3, db=db)
    factory.observable.create_or_read(
        type="type3", value="value3", parent_analysis=alert3.root_analysis, tags=["observable3_tag"], db=db
    )

    result = crud.event.read_all(tags="event1_tag", db=db)
    assert result == [event1]

    result = crud.event.read_all(tags="alert2_tag", db=db)
    assert result == [event2]

    result = crud.event.read_all(tags="observable3_tag", db=db)
    assert result == [event3]


def test_filter_by_threat_actors(db):
    event1 = factory.event.create_or_read(name="event1", threat_actors=["event1_actor"], db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(event=event2, threat_actors=["alert2_actor"], db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(event=event3, db=db)
    factory.observable.create_or_read(
        type="type3", value="value3", parent_analysis=alert3.root_analysis, threat_actors=["observable3_actor"], db=db
    )

    result = crud.event.read_all(threat_actors="event1_actor", db=db)
    assert result == [event1]

    result = crud.event.read_all(threat_actors="alert2_actor", db=db)
    assert result == [event2]

    result = crud.event.read_all(threat_actors="observable3_actor", db=db)
    assert result == [event3]


def test_filter_by_threats(db):
    event1 = factory.event.create_or_read(name="event1", threats=["event1_actor"], db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(event=event2, threats=["alert2_actor"], db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(event=event3, db=db)
    factory.observable.create_or_read(
        type="type3", value="value3", parent_analysis=alert3.root_analysis, threats=["observable3_actor"], db=db
    )

    result = crud.event.read_all(threats="event1_actor", db=db)
    assert result == [event1]

    result = crud.event.read_all(threats="alert2_actor", db=db)
    assert result == [event2]

    result = crud.event.read_all(threats="observable3_actor", db=db)
    assert result == [event3]


def test_filter_by_vectors(db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", vectors=["vector3"], db=db)

    result = crud.event.read_all(vectors="vector3", db=db)
    assert result == [event3]


def test_sort_by_created_time(db):
    now = crud.helpers.utcnow()

    event1 = factory.event.create_or_read(name="event1", created_time=now - timedelta(seconds=5), db=db)
    event2 = factory.event.create_or_read(name="event2", created_time=now, db=db)
    event3 = factory.event.create_or_read(name="event3", created_time=now + timedelta(seconds=5), db=db)

    result = crud.event.read_all(sort="created_time|asc", db=db)
    assert result == [event1, event2, event3]

    result = crud.event.read_all(sort="created_time|desc", db=db)
    assert result == [event3, event2, event1]


def test_sort_by_event_type(db):
    event1 = factory.event.create_or_read(name="event1", event_type="type1", db=db)
    event2 = factory.event.create_or_read(name="event2", event_type="type2", db=db)
    event3 = factory.event.create_or_read(name="event3", event_type="type3", db=db)

    result = crud.event.read_all(sort="event_type|asc", db=db)
    assert result == [event1, event2, event3]

    result = crud.event.read_all(sort="event_type|desc", db=db)
    assert result == [event3, event2, event1]


def test_sort_by_name(db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    event2 = factory.event.create_or_read(name="event2", db=db)
    event3 = factory.event.create_or_read(name="event3", db=db)

    result = crud.event.read_all(sort="name|asc", db=db)
    assert result == [event1, event2, event3]

    result = crud.event.read_all(sort="name|desc", db=db)
    assert result == [event3, event2, event1]


def test_sort_by_owner(db):
    event1 = factory.event.create_or_read(name="event1", owner="analyst1", db=db)
    event2 = factory.event.create_or_read(name="event2", owner="analyst2", db=db)
    event3 = factory.event.create_or_read(name="event3", owner="analyst3", db=db)

    result = crud.event.read_all(sort="owner|asc", db=db)
    assert result == [event1, event2, event3]

    result = crud.event.read_all(sort="owner|desc", db=db)
    assert result == [event3, event2, event1]


def test_sort_by_risk_level(db):
    event1 = factory.event.create_or_read(name="event1", risk_level="level1", db=db)
    event2 = factory.event.create_or_read(name="event2", risk_level="level2", db=db)
    event3 = factory.event.create_or_read(name="event3", risk_level="level3", db=db)

    result = crud.event.read_all(sort="risk_level|asc", db=db)
    assert result == [event1, event2, event3]

    result = crud.event.read_all(sort="risk_level|desc", db=db)
    assert result == [event3, event2, event1]


def test_sort_by_status(db):
    event1 = factory.event.create_or_read(name="event1", status="status1", db=db)
    event2 = factory.event.create_or_read(name="event2", status="status2", db=db)
    event3 = factory.event.create_or_read(name="event3", status="status3", db=db)

    result = crud.event.read_all(sort="status|asc", db=db)
    assert result == [event1, event2, event3]

    result = crud.event.read_all(sort="status|desc", db=db)
    assert result == [event3, event2, event1]


def test_read_analysis_type_from_event(db):
    event = factory.event.create_or_read(name="event1", db=db)

    alert1 = factory.submission.create(event=event, db=db)
    observable1 = factory.observable.create_or_read(
        type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db
    )
    analysis1 = factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="module1", db=db),
        submission=alert1,
        target=observable1,
        db=db,
    )

    result = crud.event.read_analysis_type_from_event(analysis_module_type="module1", uuid=event.uuid, db=db)
    assert result == [(alert1.uuid, analysis1)]

    alert2 = factory.submission.create(event=event, db=db)
    observable2 = factory.observable.create_or_read(
        type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db
    )
    analysis2 = factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="module2", db=db),
        submission=alert2,
        target=observable2,
        db=db,
    )

    result = crud.event.read_analysis_type_from_event(
        analysis_module_type="module", uuid=event.uuid, starts_with=True, db=db
    )
    assert result == [(alert1.uuid, analysis1), (alert2.uuid, analysis2)]


def test_read_by_uuid(db):
    event = factory.event.create_or_read(name="event1", db=db)

    alert1 = factory.submission.create(event=event, db=db)
    observable1 = factory.observable.create_or_read(
        type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="module1", db=db),
        submission=alert1,
        target=observable1,
        db=db,
    )

    alert2 = factory.submission.create(event=event, db=db)
    observable2 = factory.observable.create_or_read(
        type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="module2", db=db),
        submission=alert2,
        target=observable2,
        db=db,
    )

    result = crud.event.read_by_uuid(uuid=event.uuid, db=db)
    assert result == event
    assert not getattr(result, "analysis_types", False)

    result = crud.event.read_by_uuid(uuid=event.uuid, inject_analysis_types=True, db=db)
    assert result == event
    assert result.analysis_types == ["module1", "module2"]


def test_read_observable_type_from_event(db):
    event = factory.event.create_or_read(name="event1", db=db)

    alert1 = factory.submission.create(event=event, db=db)
    observable1 = factory.observable.create_or_read(
        type="type1", value="value1", parent_analysis=alert1.root_analysis, db=db
    )

    alert2 = factory.submission.create(event=event, db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert2.root_analysis, db=db)

    assert crud.event.read_observable_type_from_event(observable_type="type1", uuid=event.uuid, db=db) == [observable1]


def test_read_summary_detection_point(db):
    event = factory.event.create_or_read(name="event1", db=db)

    alert1 = factory.submission.create(event=event, db=db)
    factory.observable.create_or_read(
        type="type1", value="value1", parent_analysis=alert1.root_analysis, detection_points=["detection_point1"], db=db
    )

    alert2 = factory.submission.create(event=event, db=db)
    factory.observable.create_or_read(
        type="type2", value="value2", parent_analysis=alert2.root_analysis, detection_points=["detection_point2"], db=db
    )
    factory.observable.create_or_read(
        type="type3", value="value3", parent_analysis=alert2.root_analysis, detection_points=["detection_point2"], db=db
    )

    result = crud.event.read_summary_detection_point(uuid=event.uuid, db=db)
    assert len(result) == 2
    assert result[0].alert_uuid == alert1.uuid
    assert result[0].count == 1
    assert result[0].value == "detection_point1"
    assert result[1].alert_uuid == alert2.uuid
    assert result[1].count == 2
    assert result[1].value == "detection_point2"


def test_read_summary_email(db):
    now = crud.helpers.utcnow()

    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The email summary should be empty
    assert crud.event.read_summary_email(uuid=event.uuid, db=db) == []

    # Add some alerts with analysis to the event
    #
    # alert1
    #   o1
    #     a1 - email analysis 1
    #
    # alert2
    #  o1
    #    a1 - email analysis 2
    #
    # alert3
    #  o1
    #    a1 - email analysis 2
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="file",
        value="6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        parent_analysis=alert1.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "blah",
            "message_id": "<abcd1234@evil.com>",
            "subject": "Hello",
            "time": now.isoformat(),
            "to_address": "goodguy@company.com",
        },
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="file",
        value="d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
        parent_analysis=alert2.root_analysis,
        db=db,
    )
    time = (now + timedelta(minutes=5)).isoformat()
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert2,
        target=alert2_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "blah",
            "message_id": "<1234abcd@evil.com>",
            "subject": "Hello",
            "time": time,
            "to_address": "otherguy@company.com",
        },
    )

    # Add a third alert that has the exact same analysis as one of the others
    alert3 = factory.submission.create(db=db, event=event)
    alert3_o1 = factory.observable.create_or_read(
        type="file",
        value="d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
        parent_analysis=alert3.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert3,
        target=alert3_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "blah",
            "message_id": "<1234abcd@evil.com>",
            "subject": "Hello",
            "time": time,
            "to_address": "otherguy@company.com",
        },
    )

    # Add a fourth alert that is not part of the event
    alert4 = factory.submission.create(db=db)
    alert4_o1 = factory.observable.create_or_read(
        type="file",
        value="4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce",
        parent_analysis=alert4.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert4,
        target=alert4_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "neutralguy@okay.com",
            "headers": "blah",
            "message_id": "<1234abcd@okay.com>",
            "subject": "Hi",
            "time": now.isoformat(),
            "to_address": "goodguy@company.com",
        },
    )

    # The email summary should now have two entries in it. Even though one of the emails was repeated two
    # times across the alerts, its Email Analysis is going to be the same for each, so it appears once in the summary.
    # Additionally, the results should be sorted by the email time.
    result = crud.event.read_summary_email(uuid=event.uuid, db=db)
    assert len(result) == 2
    assert result[0].message_id == "<abcd1234@evil.com>"
    assert result[1].message_id == "<1234abcd@evil.com>"


def test_read_summary_email_headers_body(db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The email headers/body summary should be empty
    crud.event.read_summary_email_headers_body(uuid=event.uuid, db=db) == []

    # Add some alerts with analysis to the event
    #
    # alert1
    #   o1
    #     a1 - email analysis 1
    #
    # alert2
    #  o1
    #    a1 - email analysis 2
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="file",
        value="6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        parent_analysis=alert1.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
        details={
            "attachments": [],
            "body_html": "<p>body1</p>",
            "body_text": "body1",
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "headers1",
            "message_id": "<abcd1234@evil.com>",
            "subject": "Hello",
            "time": crud.helpers.utcnow().isoformat(),
            "to_address": "goodguy@company.com",
        },
    )

    # The second alert's email has an earlier time
    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="file",
        value="d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
        parent_analysis=alert2.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert2,
        target=alert2_o1,
        details={
            "attachments": [],
            "body_html": "<p>body2</p>",
            "body_text": "body2",
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "headers2",
            "message_id": "<1234abcd@evil.com>",
            "subject": "Hello",
            "time": (crud.helpers.utcnow() - timedelta(days=1)).isoformat(),
            "to_address": "otherguy@company.com",
        },
    )

    # Add an alert that is not part of the event
    alert3 = factory.submission.create(db=db)
    alert3_o1 = factory.observable.create_or_read(
        type="file",
        value="4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce",
        parent_analysis=alert3.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert3,
        target=alert3_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "neutralguy@okay.com",
            "headers": "blah",
            "message_id": "<1234abcd@okay.com>",
            "subject": "Hi",
            "time": crud.helpers.utcnow().isoformat(),
            "to_address": "goodguy@company.com",
        },
    )

    # The email headers/body summary should now have the details of the second alert's email
    result = crud.event.read_summary_email_headers_body(uuid=event.uuid, db=db)
    assert result.alert_uuid == alert2.uuid
    assert result.headers == "headers2"
    assert result.body_html == "<p>body2</p>"
    assert result.body_text == "body2"


def test_read_summary_observable(db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The observable summary should be empty
    assert crud.event.read_summary_observable(uuid=event.uuid, db=db) == []

    # Add some alerts with analyses to the event
    #
    # alert1
    #   o1
    #     a1
    #       o2 - 127.0.0.1
    #         a2 - FA Q
    #   o3 - 127.0.0.1
    #     a3 - FA Q
    #
    # alert2
    #  o1 - 127.0.0.1
    #    a1 - FA Q
    #  o2 - 192.168.1.1
    #    a2 - FA Q
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="fqdn", value="localhost.localdomain", parent_analysis=alert1.root_analysis, db=db
    )
    alert1_a1 = factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FQDN Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
    )
    alert1_o2 = factory.observable.create_or_read(type="ipv4", value="127.0.0.1", parent_analysis=alert1_a1, db=db)
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 1", db=db),
        submission=alert1,
        target=alert1_o2,
        details={"link": "https://url.to.search/query=asdf", "hits": 10},
    )
    alert1_o3 = factory.observable.create_or_read(
        type="ipv4", value="127.0.0.1", parent_analysis=alert1.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 1", db=db),
        submission=alert1,
        target=alert1_o3,
        details={"link": "https://url.to.search/query=asdf", "hits": 10},
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="ipv4", value="127.0.0.1", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 1", db=db),
        submission=alert2,
        target=alert2_o1,
        details={"link": "https://url.to.search/query=asdf", "hits": 10},
    )
    alert2_o2 = factory.observable.create_or_read(
        type="ipv4", value="192.168.1.1", parent_analysis=alert2.root_analysis, db=db
    )
    # This FA Queue analysis doesn't have a "link" field
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 2", db=db),
        submission=alert2,
        target=alert2_o2,
        details={"hits": 100},
    )

    # Add a third alert that is not part of the event
    alert3 = factory.submission.create(db=db)
    alert3_o1 = factory.observable.create_or_read(
        type="ipv4", value="172.16.1.1", parent_analysis=alert3.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 1", db=db),
        submission=alert3,
        target=alert3_o1,
        details={"link": "https://url.to.search/query=asdf", "hits": 0},
    )

    # The observable summary should now have two entries in it. Even though the 127.0.0.1 observable was repeated three
    # times across the two alerts, its FA Queue Analysis is going to be the same for each, so it appears once in the summary.
    # Additionally, the results should be sorted by their type then value.
    result = crud.event.read_summary_observable(uuid=event.uuid, db=db)
    assert len(result) == 2
    assert result[0].value == "127.0.0.1"
    assert result[0].faqueue_hits == 10
    assert result[1].value == "192.168.1.1"
    assert result[1].faqueue_hits == 100


def test_read_summary_sandbox(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The sandbox summary should be empty
    assert crud.event.read_summary_sandbox(uuid=event.uuid, db=db) == []

    # Define the sandbox analysis details that will be used in the alerts
    sample1_details = SandboxAnalysisDetails(
        contacted_hosts=[
            SandboxContactedHost(
                ip="127.0.0.1",
                port=80,
                protocol="TCP",
                location="some place",
                associated_domains=["domain1", "domain2"],
            ),
            SandboxContactedHost(
                ip="192.168.1.1", port=443, protocol="TCP", location="some other place", associated_domains=[]
            ),
        ],
        created_services=["created_service1", "created_service2"],
        dns_requests=[
            SandboxDnsRequest(request="malware.com", type="A", answer="127.0.0.1", answer_type="A"),
            SandboxDnsRequest(request="othermalware.com", type="A", answer="192.168.1.1", answer_type="A"),
        ],
        dropped_files=[
            SandboxDroppedFile(
                filename="dropped1.exe",
                path="c:\\users\\analyst\\desktop\\dropped1.exe",
                size=100,
                type="application/octet-stream",
                md5="10239eb7264449296277d10538e27f3e",
                sha1="344329cc1356f227a722ad81e36a6e5baf6a0642",
                sha256="17d771db597ca8eb06c874200a067d7ac4374aa14d7b775a3b57181e69cfb100",
                sha512="54f61aba3cfb0249b84b9b2464b946e1039615dbebe6ce2ca6403c91945ef30a6156eb5c3ec330fe8c67b34e8a8b71a2f6e8d394874a72dd06fb96649d020682",
                ssdeep="3:cIoN:cb",
            ),
            SandboxDroppedFile(
                filename="dropped2.exe",
                path="c:\\users\\analyst\\desktop\\dropped2.exe",
                size=100,
                type="application/octet-stream",
                md5="8ad98e2965070ebbb86a95e35c18010f",
                sha1="6e1833d62213441c60edce1a4cfb6674af102d69",
                sha256="fc0fefa8d1f318419f927bc3b793bf66a035d59f24874ce7cf773f9162d0a158",
                sha512="6774d837fb2851c1c1d89170068caa1b81143b81ec7fbf4322b3ffdbc24efcebcc12d763d1c6f4b0c843e43427671453167b1c50ed5f71c7ede8759f75f39732",
                ssdeep="3:cIeAn:ckn",
            ),
        ],
        filename="malware.exe",
        http_requests=[
            SandboxHttpRequest(
                host="malware.com",
                port=80,
                path="/malware.exe",
                method="GET",
                user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
            ),
            SandboxHttpRequest(
                host="othermalware.com",
                port=443,
                path="/othermalware.exe",
                method="GET",
                user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
            ),
        ],
        malware_family="ransomware",
        md5="9051c29972c935649d8fa4b823e54dea",
        memory_strings=["memory_string1", "memory_string2"],
        memory_urls=["http://memory.url1", "http://memory.url2"],
        mutexes=["mutex1", "mutex2"],
        processes=[
            SandboxProcess(command="malware.exe", pid=1000, parent_pid=0),
            SandboxProcess(command="sub_command1", pid=1001, parent_pid=1000),
            SandboxProcess(command="sub_sub_command", pid=1002, parent_pid=1001),
            SandboxProcess(command="sub_command2", pid=1003, parent_pid=1000),
        ],
        registry_keys=["registry_key1", "registry_key2"],
        resolved_apis=["resolved_api1", "resolved_api2"],
        sandbox_url="https://url.to.sandbox.report",
        sha1="2da7b04fa4f6e94c7c82c1c8ee09ead16121bc60",
        sha256="66ecfc29b6d458538b23310988289158f319e2e1cf7587413011d43a639c6ec0",
        sha512="951c56c1bad4cdb721da736d9f1c04ebbbf32d2737c8ec8c64086a4c5448cb37f95784186c8c67c42b7bc622ba6358dc8befee750c14bcf5136a6706a19e007b",
        ssdeep="3:5c+a:q",
        started_services=["started_service1", "started_service2"],
        strings_urls=["https://string.url1", "https://string.url2"],
        suricata_alerts=["suricata_alert1", "suricata_alert2"],
    )

    sample2_details = SandboxAnalysisDetails(
        filename="othermalware.exe",
        md5="be0910beda52d3c1552822c43345061a",
        sandbox_url="https://url.to.other.sandbox.report",
        sha1="534cc9232929857e8b84236a4f955c9b5d303a7d",
        sha256="73b4ed99444440ad52ad2bb8da8ee7d186d4b31705783c0b8f45ada7007bfd1c",
    )

    sample3_details = SandboxAnalysisDetails(
        filename="good.exe",
        md5="93ac743902fa30840d4cd30a52068a78",
        sandbox_url="https://url.to.sandbox.report",
    )

    # Add some alerts with sandbox analysis to the event
    #
    # alert1
    #   o1
    #     a1 - Sandbox Analysis (malware.exe)
    #
    # alert2
    #   o1
    #     a1 - Sandbox Analysis (malware.exe)
    #   o2
    #     a2 - Sandbox Analysis (othermalware.exe)
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="file", value="malware.exe", parent_analysis=alert1.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Sandbox Analysis - Sandbox 1", db=db),
        submission=alert1,
        target=alert1_o1,
        details=json.loads(sample1_details.json()),
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="file", value="malware.exe", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Sandbox Analysis - Sandbox 1", db=db),
        submission=alert2,
        target=alert2_o1,
        details=json.loads(sample1_details.json()),
    )
    alert2_o2 = factory.observable.create_or_read(
        type="file", value="othermalware.exe", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Sandbox Analysis - Sandbox 2", db=db),
        submission=alert2,
        target=alert2_o2,
        details=json.loads(sample2_details.json()),
    )

    # Add a third alert that is not part of the event
    alert3 = factory.submission.create(db=db)
    alert3_o1 = factory.observable.create_or_read(
        type="file", value="good.exe", parent_analysis=alert3.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Sandbox Analysis - Sandbox 1", db=db),
        submission=alert3,
        target=alert3_o1,
        details=json.loads(sample3_details.json()),
    )

    # The sandbox summary should now have two entries in it. The malware.exe report is repeated, so it
    # only counts once for the purposes of the summary.
    # Additionally, the results should be sorted by the filenames.
    result = crud.event.read_summary_sandbox(uuid=event.uuid, db=db)
    assert len(result) == 2
    assert result[0].filename == "malware.exe"
    assert result[0].process_tree == "malware.exe\n    sub_command1\n        sub_sub_command\n    sub_command2"
    assert result[1].filename == "othermalware.exe"
    assert result[1].process_tree == ""


def test_read_summary_url_domain(db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The URL domains summary should be empty
    assert crud.event.read_summary_url_domain(uuid=event.uuid, db=db) == URLDomainSummary(domains=[], total=0)

    # Add some alerts with analyses to the event
    #
    # alert1
    #   o1 - https://example.com
    #     a1
    #       o2 - https://example2.com
    #       o3 - https://example.com
    #
    # alert2
    #  o1 - https://example.com/index.html
    #  o2 - https://example3.com
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="url", value="https://example.com", parent_analysis=alert1.root_analysis, db=db
    )
    alert1_a1 = factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="URL Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
    )
    factory.observable.create_or_read(type="url", value="https://example2.com", parent_analysis=alert1_a1, db=db)
    factory.observable.create_or_read(type="url", value="https://example.com", parent_analysis=alert1_a1, db=db)

    alert2 = factory.submission.create(db=db, event=event)
    factory.observable.create_or_read(
        type="url", value="https://example.com/index.html", parent_analysis=alert2.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example3.com", parent_analysis=alert2.root_analysis, db=db
    )

    # Add a third alert that is not part of the event
    alert3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="url", value="https://example4.com", parent_analysis=alert3.root_analysis, db=db
    )

    # The URL domain summary should now have three entries in it. The https://example.com URL is repeated, so it
    # only counts once for the purposes of the summary.
    # Additionally, the results should be sorted by the number of times the domains appeared then by the domain.
    #
    # Results: example.com (2), example2.com (1), example3.com (1)
    result = crud.event.read_summary_url_domain(uuid=event.uuid, db=db)
    assert result.total == 4
    assert len(result.domains) == 3
    assert result.domains[0].domain == "example.com"
    assert result.domains[0].count == 2
    assert result.domains[1].domain == "example2.com"
    assert result.domains[1].count == 1
    assert result.domains[2].domain == "example3.com"
    assert result.domains[2].count == 1


def test_read_summary_user(db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The user summary should be empty
    assert crud.event.read_summary_user(uuid=event.uuid, db=db) == []

    # Add some alerts with analyses to the event
    #
    # alert1
    #   o1
    #     a1 - user1 analysis
    #
    # alert2
    #  o1
    #    a1 - user2 analysis
    #
    # alert3
    #  o1
    #    a1 - user1 analysis

    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="email_address", value="goodguy@company.com", parent_analysis=alert1.root_analysis, db=db
    )
    # This analysis is missing the optional "manager_email" key
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="User Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
        details={
            "user_id": "12345",
            "email": "goodguy@company.com",
            "company": "Company Inc.",
            "division": "R&D",
            "department": "Widgets",
            "title": "Director",
        },
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="email_address", value="otherguy@company.com", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="User Analysis", db=db),
        submission=alert2,
        target=alert2_o1,
        details={
            "user_id": "98765",
            "email": "otherguy@company.com",
            "company": "Company Inc.",
            "division": "R&D",
            "department": "Widgets",
            "title": "Engineer",
            "manager_email": "goodguy@company.com",
        },
    )

    alert3 = factory.submission.create(db=db, event=event)
    alert3_o1 = factory.observable.create_or_read(
        type="email_address", value="goodguy@company.com", parent_analysis=alert3.root_analysis, db=db
    )
    # This analysis is missing the optional "manager_email" key
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="User Analysis", db=db),
        submission=alert3,
        target=alert3_o1,
        details={
            "user_id": "12345",
            "email": "goodguy@company.com",
            "company": "Company Inc.",
            "division": "R&D",
            "department": "Widgets",
            "title": "Director",
        },
    )

    # Add a fourth alert that is not part of the event
    alert4 = factory.submission.create(db=db)
    alert4_o1 = factory.observable.create_or_read(
        type="email_address", value="dude@company.com", parent_analysis=alert4.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="User Analysis", db=db),
        submission=alert4,
        target=alert4_o1,
        details={
            "user_id": "abcde",
            "email": "dude@company.com",
            "company": "Company Inc.",
            "division": "Finance",
            "department": "Widgets",
            "title": "Accountant",
            "manager_email": "manager@company.com",
        },
    )

    # The user summary should now have two entries in it. Even though one user's analysis was repeated two
    # times across the alerts, its User Analysis is going to be the same for each, so it appears once in the summary.
    # Additionally, the results should be sorted by their email.
    result = crud.event.read_summary_user(uuid=event.uuid, db=db)
    assert len(result) == 2
    assert result[0].email == "goodguy@company.com"
    assert result[0].manager_email is None
    assert result[1].email == "otherguy@company.com"
