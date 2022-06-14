from datetime import timedelta

from api_models.observable import ObservableCreateInSubmission
from api_models.submission import SubmissionUpdate
from api_models.summaries import URLDomainSummary
from db import crud
from tests import factory


def test_filter_by_alert(db):
    submission1 = factory.submission.create(alert=True, db=db)
    factory.submission.create(alert=False, db=db)

    result = crud.submission.read_all(alert=True, db=db)
    assert result == [submission1]


def test_filter_by_disposition(db):
    submission1 = factory.submission.create(disposition="DELIVERY", db=db)
    submission2 = factory.submission.create(db=db)

    result = crud.submission.read_all(disposition="DELIVERY", db=db)
    assert result == [submission1]

    result = crud.submission.read_all(disposition="none", db=db)
    assert result == [submission2]


def test_filter_by_disposition_user(db):
    submission1 = factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        history_username="analyst",
        db=db,
    )
    factory.submission.create(db=db)

    result = crud.submission.read_all(disposition_user="analyst", db=db)
    assert result == [submission1]

    # Another analyst dispositions the same alert
    factory.alert_disposition.create_or_read(value="FALSE_POSITIVE", rank=2, db=db)
    factory.user.create_or_read(username="analyst2", db=db)
    crud.submission.update(
        model=SubmissionUpdate(disposition="FALSE_POSITIVE", history_username="analyst2", uuid=submission1.uuid), db=db
    )

    # The submission should still be returned when filtering by analyst since it uses the submission's history
    assert submission1.disposition_user.username == "analyst2"
    result = crud.submission.read_all(disposition_user="analyst", db=db)
    assert result == [submission1]


def test_filter_by_dispositioned_after(db):
    now = crud.helpers.utcnow()

    factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now - timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )
    factory.submission.create(
        disposition="DELIVERY", updated_by_user="analyst", update_time=now, history_username="analyst", db=db
    )
    submission3 = factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now + timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )

    result = crud.submission.read_all(dispositioned_after=now, db=db)
    assert result == [submission3]


def test_filter_by_dispositioned_before(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now - timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )
    factory.submission.create(
        disposition="DELIVERY", updated_by_user="analyst", update_time=now, history_username="analyst", db=db
    )
    factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now + timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )

    result = crud.submission.read_all(dispositioned_before=now, db=db)
    assert result == [submission1]


def test_filter_by_event_time_after(db):
    now = crud.helpers.utcnow()

    factory.submission.create(event_time=now - timedelta(seconds=5), db=db)
    factory.submission.create(event_time=now, db=db)
    submission3 = factory.submission.create(event_time=now + timedelta(seconds=5), db=db)

    result = crud.submission.read_all(event_time_after=now, db=db)
    assert result == [submission3]


def test_filter_by_event_time_before(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(event_time=now - timedelta(seconds=5), db=db)
    factory.submission.create(event_time=now, db=db)
    factory.submission.create(event_time=now + timedelta(seconds=5), db=db)

    result = crud.submission.read_all(event_time_before=now, db=db)
    assert result == [submission1]


def test_filter_by_event_uuid(db):
    event = factory.event.create_or_read(name="test", db=db)
    submission1 = factory.submission.create(event=event, db=db)
    factory.submission.create(db=db)

    result = crud.submission.read_all(event_uuid=event.uuid, db=db)
    assert result == [submission1]


def test_filter_by_insert_time_after(db):
    now = crud.helpers.utcnow()

    factory.submission.create(insert_time=now - timedelta(seconds=5), db=db)
    factory.submission.create(insert_time=now, db=db)
    submission3 = factory.submission.create(insert_time=now + timedelta(seconds=5), db=db)

    result = crud.submission.read_all(insert_time_after=now, db=db)
    assert result == [submission3]


def test_filter_by_insert_time_before(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(insert_time=now - timedelta(seconds=5), db=db)
    factory.submission.create(insert_time=now, db=db)
    factory.submission.create(insert_time=now + timedelta(seconds=5), db=db)

    result = crud.submission.read_all(insert_time_before=now, db=db)
    assert result == [submission1]


def test_filter_by_name(db):
    submission1 = factory.submission.create(name="submission1", db=db)
    submission2 = factory.submission.create(name="submission2", db=db)

    result = crud.submission.read_all(name="submission1", db=db)
    assert result == [submission1]

    result = crud.submission.read_all(name="submission", db=db)
    assert result == [submission1, submission2]


def test_filter_by_observable(db):
    factory.observable_type.create_or_read(value="type", db=db)

    submission1 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type", value="value")], db=db
    )

    factory.submission.create(observables=[ObservableCreateInSubmission(type="type", value="value2")], db=db)

    result = crud.submission.read_all(observable="type|value", db=db)
    assert result == [submission1]


def test_filter_by_observable_types(db):
    factory.observable_type.create_or_read(value="type", db=db)
    factory.observable_type.create_or_read(value="type2", db=db)

    submission1 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type", value="value")], db=db
    )

    factory.submission.create(observables=[ObservableCreateInSubmission(type="type2", value="value2")], db=db)

    result = crud.submission.read_all(observable_types="type", db=db)
    assert result == [submission1]


def test_filter_by_observable_value(db):
    factory.observable_type.create_or_read(value="type", db=db)

    submission1 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type", value="value")], db=db
    )

    factory.submission.create(observables=[ObservableCreateInSubmission(type="type", value="value2")], db=db)

    result = crud.submission.read_all(observable_value="value", db=db)
    assert result == [submission1]


def test_filter_by_owner(db):
    submission1 = factory.submission.create(owner="analyst", db=db)
    factory.submission.create(db=db)

    result = crud.submission.read_all(owner="analyst", db=db)
    assert result == [submission1]


def test_filter_by_queue(db):
    submission1 = factory.submission.create(alert_queue="queue1", db=db)
    factory.submission.create(alert_queue="queue2", db=db)

    result = crud.submission.read_all(queue="queue1", db=db)
    assert result == [submission1]


def test_filter_by_tags(db):
    submission1 = factory.submission.create(db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission1.root_analysis, db=db)

    submission2 = factory.submission.create(tags=["submission2_tag"], db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=submission2.root_analysis, db=db)

    submission3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="type3", value="value3", parent_analysis=submission3.root_analysis, tags=["observable3_tag"], db=db
    )

    result = crud.submission.read_all(tags="submission2_tag", db=db)
    assert result == [submission2]

    result = crud.submission.read_all(tags="observable3_tag", db=db)
    assert result == [submission3]


def test_filter_by_threat_actors(db):
    submission1 = factory.submission.create(db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission1.root_analysis, db=db)

    submission2 = factory.submission.create(threat_actors=["submission2_actor"], db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=submission2.root_analysis, db=db)

    submission3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="type3",
        value="value3",
        parent_analysis=submission3.root_analysis,
        threat_actors=["observable3_actor"],
        db=db,
    )

    result = crud.submission.read_all(threat_actors="submission2_actor", db=db)
    assert result == [submission2]

    result = crud.submission.read_all(threat_actors="observable3_actor", db=db)
    assert result == [submission3]


def test_filter_by_threats(db):
    submission1 = factory.submission.create(db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission1.root_analysis, db=db)

    submission2 = factory.submission.create(threats=["submission2_actor"], db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=submission2.root_analysis, db=db)

    submission3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="type3", value="value3", parent_analysis=submission3.root_analysis, threats=["observable3_actor"], db=db
    )

    result = crud.submission.read_all(threats="submission2_actor", db=db)
    assert result == [submission2]

    result = crud.submission.read_all(threats="observable3_actor", db=db)
    assert result == [submission3]


def test_filter_by_tool(db):
    submission1 = factory.submission.create(tool="tool1", db=db)
    factory.submission.create(tool="tool2", db=db)

    result = crud.submission.read_all(tool="tool1", db=db)
    assert result == [submission1]


def test_filter_by_tool_instance(db):
    submission1 = factory.submission.create(tool_instance="tool_instance1", db=db)
    factory.submission.create(tool_instance="tool_instance2", db=db)

    result = crud.submission.read_all(tool_instance="tool_instance1", db=db)
    assert result == [submission1]


def test_filter_by_type(db):
    submission1 = factory.submission.create(submission_type="type1", db=db)
    factory.submission.create(submission_type="type2", db=db)

    result = crud.submission.read_all(submission_type="type1", db=db)
    assert result == [submission1]


def test_read_all_history(db):
    submission = factory.submission.create(history_username="analyst", db=db)
    result = crud.submission.read_all_history(uuid=submission.uuid, db=db)
    assert len(result) == 1
    assert result[0].action == "CREATE"


def test_read_observables(db):
    # Create a submission tree where the same observable type+value appears twice
    #
    # submission
    #   o1
    #     a
    #       o1
    #   o2
    submission = factory.submission.create(db=db)
    observable1 = factory.observable.create_or_read(
        type="fqdn", value="bad.com", parent_analysis=submission.root_analysis, db=db
    )
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", db=db)
    analysis = factory.analysis.create_or_read(
        analysis_module_type=analysis_module_type, submission=submission, target=observable1, db=db
    )
    factory.observable.create_or_read(type="fqdn", value="bad.com", parent_analysis=analysis, db=db)
    factory.observable.create_or_read(type="ipv4", value="127.0.0.1", parent_analysis=submission.root_analysis, db=db)

    # Create a second submission tree with a duplicate observable from the first submission
    #
    # submission
    #   o2
    #   o3
    submission2 = factory.submission.create(db=db)
    factory.observable.create_or_read(type="ipv4", value="127.0.0.1", parent_analysis=submission2.root_analysis, db=db)
    factory.observable.create_or_read(
        type="email_address", value="badguy@bad.com", parent_analysis=submission2.root_analysis, db=db
    )

    # Fetching the list of observables in the submissions should only show three observables since
    # there were duplicates. Additionally, they should be sorted by the types then values:
    #
    # email_address: badguy@bad.com
    # fqdn: bad.com
    # ipv4: 127.0.0.1
    result = crud.submission.read_observables(uuids=[submission.uuid, submission2.uuid], db=db)
    assert len(result) == 3
    assert result[0].type.value == "email_address" and result[0].value == "badguy@bad.com"
    assert result[1].type.value == "fqdn" and result[1].value == "bad.com"
    assert result[2].type.value == "ipv4" and result[2].value == "127.0.0.1"


def test_read_submission_tree(db):
    submission = factory.submission.create_from_json_file(
        db=db, json_path="/app/tests/alerts/small.json", submission_name="Test Alert"
    )

    # The small.json submission has 14 observables and 16 analyses (the Root Analysis is not included in the tree).
    result = crud.submission.read_tree(uuid=submission.uuid, db=db)
    assert str(result["children"]).count("'observable'") == 14
    assert str(result["children"]).count("'analysis'") == 16
    assert len(result["children"]) == 2


def test_sort_by_disposition(db):
    submission1 = factory.submission.create(disposition="disposition1", db=db)
    submission2 = factory.submission.create(disposition="disposition2", db=db)
    submission3 = factory.submission.create(db=db)

    result = crud.submission.read_all(sort="disposition|asc", db=db)
    assert result == [submission1, submission2, submission3]

    result = crud.submission.read_all(sort="disposition|desc", db=db)
    assert result == [submission3, submission2, submission1]


def test_sort_by_disposition_time(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(disposition="disposition1", update_time=now - timedelta(seconds=5), db=db)
    submission2 = factory.submission.create(disposition="disposition2", update_time=now, db=db)
    submission3 = factory.submission.create(db=db)

    result = crud.submission.read_all(sort="disposition_time|asc", db=db)
    assert result == [submission1, submission2, submission3]

    result = crud.submission.read_all(sort="disposition_time|desc", db=db)
    assert result == [submission3, submission2, submission1]


def test_sort_by_disposition_user(db):
    submission1 = factory.submission.create(disposition="disposition1", updated_by_user="analyst1", db=db)
    submission2 = factory.submission.create(disposition="disposition2", updated_by_user="analyst2", db=db)
    submission3 = factory.submission.create(db=db)

    result = crud.submission.read_all(sort="disposition_user|asc", db=db)
    assert result == [submission1, submission2, submission3]

    result = crud.submission.read_all(sort="disposition_user|desc", db=db)
    assert result == [submission3, submission2, submission1]


def test_sort_by_event_time(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(event_time=now - timedelta(seconds=5), db=db)
    submission2 = factory.submission.create(event_time=now, db=db)

    result = crud.submission.read_all(sort="event_time|asc", db=db)
    assert result == [submission1, submission2]

    result = crud.submission.read_all(sort="event_time|desc", db=db)
    assert result == [submission2, submission1]


def test_sort_by_insert_time(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(insert_time=now - timedelta(seconds=5), db=db)
    submission2 = factory.submission.create(insert_time=now, db=db)

    result = crud.submission.read_all(sort="insert_time|asc", db=db)
    assert result == [submission1, submission2]

    result = crud.submission.read_all(sort="insert_time|desc", db=db)
    assert result == [submission2, submission1]


def test_sort_by_name(db):
    submission1 = factory.submission.create(name="submission1", db=db)
    submission2 = factory.submission.create(name="submission2", db=db)

    result = crud.submission.read_all(sort="name|asc", db=db)
    assert result == [submission1, submission2]

    result = crud.submission.read_all(sort="name|desc", db=db)
    assert result == [submission2, submission1]


def test_sort_by_owner(db):
    submission1 = factory.submission.create(owner="analyst1", db=db)
    submission2 = factory.submission.create(owner="analyst2", db=db)

    result = crud.submission.read_all(sort="owner|asc", db=db)
    assert result == [submission1, submission2]

    result = crud.submission.read_all(sort="owner|desc", db=db)
    assert result == [submission2, submission1]


def test_sort_by_queue(db):
    submission1 = factory.submission.create(alert_queue="queue1", db=db)
    submission2 = factory.submission.create(alert_queue="queue2", db=db)

    result = crud.submission.read_all(sort="queue|asc", db=db)
    assert result == [submission1, submission2]

    result = crud.submission.read_all(sort="queue|desc", db=db)
    assert result == [submission2, submission1]


def test_sort_by_type(db):
    submission1 = factory.submission.create(submission_type="type1", db=db)
    submission2 = factory.submission.create(submission_type="type2", db=db)

    result = crud.submission.read_all(sort="submission_type|asc", db=db)
    assert result == [submission1, submission2]

    result = crud.submission.read_all(sort="submission_type|desc", db=db)
    assert result == [submission2, submission1]


def test_read_summary_url_domain(db):
    # Create a submission
    submission1 = factory.submission.create(db=db)

    # The URL domains summary should be empty
    assert crud.submission.read_summary_url_domain(uuid=submission1.uuid, db=db) == URLDomainSummary(
        domains=[], total=0
    )

    # Add some observables to the submission
    #
    #   o1 - url - https://example.com
    #   o2 - url - https://example2.com
    #   o3 - url - https://example.com
    #   o4 - url - https://example.com/index.html
    #   o5 - url - https://example3.com
    #   o6 - ipv4 - 1.2.3.4
    #   o7 - email_address - name@company.com

    factory.observable.create_or_read(
        type="url", value="https://example.com", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example2.com", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example.com", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example.com/index.html", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example3.com", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example4.com", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(type="ipv4", value="1.2.3.4", parent_analysis=submission1.root_analysis, db=db)
    factory.observable.create_or_read(
        type="email_address", value="name@company.com", parent_analysis=submission1.root_analysis, db=db
    )

    # The URL domain summary should now have three entries in it. The https://example.com URL is repeated, so it
    # only counts once for the purposes of the summary.
    # Additionally, the results should be sorted by the number of times the domains appeared then by the domain.
    #
    # Results: example.com (2), example2.com (1), example3.com (1)
    result = crud.submission.read_summary_url_domain(uuid=submission1.uuid, db=db)
    assert result.total == 4
    assert len(result.domains) == 3
    assert result.domains[0].domain == "example.com"
    assert result.domains[0].count == 2
    assert result.domains[1].domain == "example2.com"
    assert result.domains[1].count == 1
    assert result.domains[2].domain == "example3.com"
    assert result.domains[2].count == 1
