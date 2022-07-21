from datetime import timedelta
from re import sub

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
    submission3 = factory.submission.create(disposition="FALSE_POSITIVE", db=db)

    # disposition
    result = crud.submission.read_all(disposition=["DELIVERY"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(disposition=["none"], db=db)
    assert result == [submission2]

    result = crud.submission.read_all(disposition=["DELIVERY", "none"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_disposition
    result = crud.submission.read_all(not_disposition=["DELIVERY"], db=db)
    assert len(result) == 2
    assert submission2 in result
    assert submission3 in result

    result = crud.submission.read_all(not_disposition=["none"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission3 in result

    result = crud.submission.read_all(not_disposition=["DELIVERY", "none"], db=db)
    assert result == [submission3]

    # conflicting
    assert crud.submission.read_all(disposition=["FALSE_POSITIVE"], not_disposition=["FALSE_POSITIVE"], db=db) == []


def test_filter_by_disposition_user(db):
    submission1 = factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        history_username="analyst",
        db=db,
    )
    submission2 = factory.submission.create(db=db)

    # disposition_user
    assert crud.submission.read_all(disposition_user=["none"], db=db) == [submission2]

    result = crud.submission.read_all(disposition_user=["none", "analyst"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    result = crud.submission.read_all(disposition_user=["analyst"], db=db)
    assert result == [submission1]

    # Another analyst dispositions the same alert
    factory.alert_disposition.create_or_read(value="FALSE_POSITIVE", rank=2, db=db)
    factory.user.create_or_read(username="analyst2", db=db)
    crud.submission.update(
        model=SubmissionUpdate(disposition="FALSE_POSITIVE", history_username="analyst2", uuid=submission1.uuid), db=db
    )

    # The submission should still be returned when filtering by analyst since it uses the submission's history
    assert submission1.disposition_user.username == "analyst2"
    result = crud.submission.read_all(disposition_user=["analyst"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(disposition_user=["analyst", "analyst2"], db=db)
    assert result == [submission1]

    # not_disposition_user
    assert crud.submission.read_all(not_disposition_user=["none"], db=db) == [submission1]
    assert crud.submission.read_all(not_disposition_user=["none", "analyst"], db=db) == []
    assert crud.submission.read_all(not_disposition_user=["analyst", "analyst2"], db=db) == [submission2]


def test_filter_by_dispositioned_after(db):
    now = crud.helpers.utcnow()

    factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now - timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )
    submission2 = factory.submission.create(
        disposition="DELIVERY", updated_by_user="analyst", update_time=now, history_username="analyst", db=db
    )
    submission3 = factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now + timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )

    result = crud.submission.read_all(dispositioned_after=[now], db=db)
    assert result == [submission3]

    result = crud.submission.read_all(dispositioned_after=[now, now - timedelta(seconds=5)], db=db)
    assert len(result) == 2
    assert submission2 in result
    assert submission3 in result


def test_filter_by_dispositioned_before(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now - timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )
    submission2 = factory.submission.create(
        disposition="DELIVERY", updated_by_user="analyst", update_time=now, history_username="analyst", db=db
    )
    factory.submission.create(
        disposition="DELIVERY",
        updated_by_user="analyst",
        update_time=now + timedelta(seconds=5),
        history_username="analyst",
        db=db,
    )

    result = crud.submission.read_all(dispositioned_before=[now], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(dispositioned_before=[now, now + timedelta(seconds=5)], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result


def test_filter_by_event_time_after(db):
    now = crud.helpers.utcnow()

    factory.submission.create(event_time=now - timedelta(seconds=5), db=db)
    submission2 = factory.submission.create(event_time=now, db=db)
    submission3 = factory.submission.create(event_time=now + timedelta(seconds=5), db=db)

    result = crud.submission.read_all(event_time_after=[now], db=db)
    assert result == [submission3]

    result = crud.submission.read_all(event_time_after=[now, now - timedelta(seconds=5)], db=db)
    assert len(result) == 2
    assert submission2 in result
    assert submission3 in result


def test_filter_by_event_time_before(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(event_time=now - timedelta(seconds=5), db=db)
    submission2 = factory.submission.create(event_time=now, db=db)
    factory.submission.create(event_time=now + timedelta(seconds=5), db=db)

    result = crud.submission.read_all(event_time_before=[now], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(event_time_before=[now, now + timedelta(seconds=5)], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result


def test_filter_by_event_uuid(db):
    event = factory.event.create_or_read(name="test", db=db)
    event2 = factory.event.create_or_read(name="test 2", db=db)
    submission1 = factory.submission.create(event=event, db=db)
    submission2 = factory.submission.create(event=event2, db=db)
    submission3 = factory.submission.create(db=db)

    # event_uuid
    assert crud.submission.read_all(event_uuid=["none"], db=db) == [submission3]

    result = crud.submission.read_all(event_uuid=["none", event.uuid], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission3 in result

    result = crud.submission.read_all(event_uuid=[event.uuid], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(event_uuid=[event.uuid, event2.uuid], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_event_uuid
    result = crud.submission.read_all(not_event_uuid=["none"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    assert crud.submission.read_all(not_event_uuid=["none", event.uuid], db=db) == [submission2]
    assert crud.submission.read_all(not_event_uuid=[event.uuid, event2.uuid], db=db) == [submission3]


def test_filter_by_insert_time_after(db):
    now = crud.helpers.utcnow()

    factory.submission.create(insert_time=now - timedelta(seconds=5), db=db)
    submission2 = factory.submission.create(insert_time=now, db=db)
    submission3 = factory.submission.create(insert_time=now + timedelta(seconds=5), db=db)

    result = crud.submission.read_all(insert_time_after=[now], db=db)
    assert result == [submission3]

    result = crud.submission.read_all(insert_time_after=[now, now - timedelta(seconds=5)], db=db)
    assert len(result) == 2
    assert submission2 in result
    assert submission3 in result


def test_filter_by_insert_time_before(db):
    now = crud.helpers.utcnow()

    submission1 = factory.submission.create(insert_time=now - timedelta(seconds=5), db=db)
    submission2 = factory.submission.create(insert_time=now, db=db)
    factory.submission.create(insert_time=now + timedelta(seconds=5), db=db)

    result = crud.submission.read_all(insert_time_before=[now], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(insert_time_before=[now, now + timedelta(seconds=5)], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result


def test_filter_by_name(db):
    submission1 = factory.submission.create(name="submission1", db=db)
    submission2 = factory.submission.create(name="submission2", db=db)
    submission3 = factory.submission.create(name="some other thing", db=db)

    # name
    result = crud.submission.read_all(name=["submission1"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(name=["submission"], db=db)
    assert result == [submission1, submission2]

    result = crud.submission.read_all(name=["submission1", "submission2"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_name
    assert crud.submission.read_all(not_name=["submission"], db=db) == [submission3]
    assert crud.submission.read_all(not_name=["submission1", "submission2"], db=db) == [submission3]


def test_filter_by_observable(db):
    factory.observable_type.create_or_read(value="type", db=db)

    submission1 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type", value="value")], db=db
    )

    submission2 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type", value="value2")], db=db
    )

    submission3 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="other_type", value="other_value")], db=db
    )

    # observable
    result = crud.submission.read_all(observable=["type|value"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(observable=["type|value", "type|value2"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_observable
    result = crud.submission.read_all(not_observable=["type|value"], db=db)
    assert len(result) == 2
    assert submission2 in result
    assert submission3 in result

    assert crud.submission.read_all(not_observable=["type|value", "type|value2"], db=db) == [submission3]


def test_filter_by_observable_types(db):
    factory.observable_type.create_or_read(value="type", db=db)
    factory.observable_type.create_or_read(value="type2", db=db)

    submission1 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type", value="value")], db=db
    )

    submission2 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type2", value="value2")], db=db
    )

    submission3 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="other_type", value="other_value")], db=db
    )

    # observable_types
    result = crud.submission.read_all(observable_types=["type"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(observable_types=["type", "type2"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_observable_types
    result = crud.submission.read_all(not_observable_types=["type"], db=db)
    assert len(result) == 2
    assert submission2 in result
    assert submission3 in result

    assert crud.submission.read_all(not_observable_types=["type", "type2"], db=db) == [submission3]


def test_filter_by_observable_value(db):
    factory.observable_type.create_or_read(value="type", db=db)

    submission1 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type", value="value")], db=db
    )

    submission2 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="type", value="value2")], db=db
    )

    submission3 = factory.submission.create(
        observables=[ObservableCreateInSubmission(type="other_type", value="other_value")], db=db
    )

    # observable_value
    result = crud.submission.read_all(observable_value=["value"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(observable_value=["value", "value2"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_observable_value
    result = crud.submission.read_all(not_observable_value=["value"], db=db)
    assert len(result) == 2
    assert submission2 in result
    assert submission3 in result

    assert crud.submission.read_all(not_observable_value=["value", "value2"], db=db) == [submission3]


def test_filter_by_owner(db):
    submission1 = factory.submission.create(owner="analyst", db=db)
    submission2 = factory.submission.create(db=db)
    submission3 = factory.submission.create(owner="analyst2", db=db)

    # owner
    result = crud.submission.read_all(owner=["analyst"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(owner=["none"], db=db)
    assert result == [submission2]

    result = crud.submission.read_all(owner=["none", "analyst"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_owner
    result = crud.submission.read_all(not_owner=["none"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission3 in result

    assert crud.submission.read_all(not_owner=["none", "analyst2"], db=db) == [submission1]
    assert crud.submission.read_all(not_owner=["analyst", "analyst2"], db=db) == [submission2]


def test_filter_by_queue(db):
    submission1 = factory.submission.create(alert_queue="queue1", db=db)
    submission2 = factory.submission.create(alert_queue="queue2", db=db)
    submission3 = factory.submission.create(db=db)

    # queue
    result = crud.submission.read_all(queue=["queue1"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(queue=["queue1", "queue2"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_queue
    assert crud.submission.read_all(not_queue=["queue1", "queue2"], db=db) == [submission3]


def test_filter_by_tags(db):
    # Create various submissions to test filtering by tags. These are the submissions that will be returned.
    submission1 = factory.submission.create(tags=["submission1_tag"], db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=submission1.root_analysis, db=db)

    submission2 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="type2",
        value="value2",
        parent_analysis=submission2.root_analysis,
        analysis_tags=["observable2_analysis_tag"],
        db=db,
    )

    submission3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="type3",
        value="value3",
        parent_analysis=submission3.root_analysis,
        tags=["observable3_tag"],
        db=db,
    )

    submission4 = factory.submission.create(tags=["submission4_tag"], db=db)
    factory.observable.create_or_read(
        type="type4",
        value="value4",
        parent_analysis=submission4.root_analysis,
        analysis_tags=["observable4_analysis_tag"],
        tags=["observable4_tag"],
        db=db,
    )

    # Create some submissions that should not be returned in the results. This is to help ensure that
    # the submission tag relationships are configured properly and do not include tags they shouldn't.
    submission5 = factory.submission.create(tags=["submission5_tag", "other_tag"], db=db)
    factory.observable.create_or_read(
        type="type5",
        value="value5",
        parent_analysis=submission5.root_analysis,
        analysis_tags=["observable5_analysis_tag"],
        tags=["observable5_tag"],
        db=db,
    )

    submission6 = factory.submission.create(tags=["submission6_tag"], db=db)
    factory.observable.create_or_read(
        type="type6", value="value6", parent_analysis=submission6.root_analysis, tags=["other_tag"], db=db
    )

    # tags

    # Verify that submission1 is returned when filtering by the "submission1_tag" tag.
    # Additionally, verify that the submission's tag relationships contain the expected tags.
    result_submission1 = crud.submission.read_all(tags=["submission1_tag"], db=db)
    assert result_submission1 == [submission1]
    assert result_submission1[0].child_analysis_tags == []
    assert result_submission1[0].child_tags == []
    assert [t.value for t in result_submission1[0].tags] == ["submission1_tag"]

    # Verify that submission2 is returned when filtering by the "observable2_analysis_tag" tag.
    # Additionally, verify that the submission's tag relationships contain the expected tags.
    result_submission2 = crud.submission.read_all(tags=["observable2_analysis_tag"], db=db)
    assert result_submission2 == [submission2]
    assert [t.value for t in result_submission2[0].child_analysis_tags] == ["observable2_analysis_tag"]
    assert result_submission2[0].child_tags == []
    assert result_submission2[0].tags == []

    # Verify that submission3 is returned when filtering by the "observable3_tag" tag.
    # Additionally, verify that the submission's tag relationships contain the expected tags.
    result_submission3 = crud.submission.read_all(tags=["observable3_tag"], db=db)
    assert result_submission3 == [submission3]
    assert result_submission3[0].child_analysis_tags == []
    assert [t.value for t in result_submission3[0].child_tags] == ["observable3_tag"]
    assert result_submission3[0].tags == []

    # Verify that submission4 is returned when filtering by the multiple tags in submission4.
    # Additionally, verify that the submission's tag relationships contain the expected tags.
    result_submission4 = crud.submission.read_all(
        tags=["submission4_tag,observable4_analysis_tag,observable4_tag"], db=db
    )
    assert result_submission4 == [submission4]
    assert [t.value for t in result_submission4[0].child_analysis_tags] == ["observable4_analysis_tag"]
    assert [t.value for t in result_submission4[0].child_tags] == ["observable4_tag"]
    assert [t.value for t in result_submission4[0].tags] == ["submission4_tag"]

    # Verify that OR filters works as expected, returning submissions that match either of the specified tags filters.
    result_submission5 = crud.submission.read_all(
        tags=["submission1_tag", "submission4_tag,observable4_analysis_tag,observable4_tag"], db=db
    )
    assert len(result_submission5) == 2
    assert submission1 in result_submission5
    assert submission4 in result_submission5

    # not_tags
    result = crud.submission.read_all(not_tags=["other_tag"], db=db)
    assert len(result) == 4
    assert submission1 in result
    assert submission2 in result
    assert submission3 in result
    assert submission4 in result

    result = crud.submission.read_all(not_tags=["submission5_tag", "submission6_tag"], db=db)
    assert len(result) == 4
    assert submission1 in result
    assert submission2 in result
    assert submission3 in result
    assert submission4 in result


def test_filter_by_tool(db):
    submission1 = factory.submission.create(tool="tool1", db=db)
    submission2 = factory.submission.create(tool="tool2", db=db)
    submission3 = factory.submission.create(tool=None, db=db)

    # tool
    assert crud.submission.read_all(tool=["none"], db=db) == [submission3]

    result = crud.submission.read_all(tool=["none", "tool1"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission3 in result

    result = crud.submission.read_all(tool=["tool1"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(tool=["tool1", "tool2"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_tool
    result = crud.submission.read_all(not_tool=["none"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    assert crud.submission.read_all(not_tool=["none", "tool2"], db=db) == [submission1]
    assert crud.submission.read_all(not_tool=["tool1", "tool2"], db=db) == [submission3]


def test_filter_by_tool_instance(db):
    submission1 = factory.submission.create(tool_instance="tool_instance1", db=db)
    submission2 = factory.submission.create(tool_instance="tool_instance2", db=db)
    submission3 = factory.submission.create(tool_instance=None, db=db)

    # tool_instance
    assert crud.submission.read_all(tool_instance=["none"], db=db) == [submission3]

    result = crud.submission.read_all(tool_instance=["none", "tool_instance1"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission3 in result

    result = crud.submission.read_all(tool_instance=["tool_instance1"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(tool_instance=["tool_instance1", "tool_instance2"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_tool_instance
    result = crud.submission.read_all(not_tool_instance=["none"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    assert crud.submission.read_all(not_tool_instance=["none", "tool_instance2"], db=db) == [submission1]
    assert crud.submission.read_all(not_tool_instance=["tool_instance1", "tool_instance2"], db=db) == [submission3]


def test_filter_by_type(db):
    submission1 = factory.submission.create(submission_type="type1", db=db)
    submission2 = factory.submission.create(submission_type="type2", db=db)
    submission3 = factory.submission.create(db=db)

    # submission_type
    result = crud.submission.read_all(submission_type=["type1"], db=db)
    assert result == [submission1]

    result = crud.submission.read_all(submission_type=["type1", "type2"], db=db)
    assert len(result) == 2
    assert submission1 in result
    assert submission2 in result

    # not_submission_type
    assert crud.submission.read_all(not_submission_type=["type1", "type2"], db=db) == [submission3]


def test_read_all_history(db):
    submission = factory.submission.create(history_username="analyst", db=db)
    result = crud.submission.read_all_history(uuid=submission.uuid, db=db)
    assert len(result) == 1
    assert result[0].action == "CREATE"


def test_read_observables(db):
    # Create a submission tree where the same observable type+value appears twice
    #
    # submission
    #   o1 - analysis_tag1, display_type1, directive1, time1
    #     a
    #       o1 - analysis_tag2
    #   o2 - analysis_tag3, tag1, display_value1
    time1 = crud.helpers.utcnow()
    submission = factory.submission.create(db=db)
    observable1 = factory.observable.create_or_read(
        type="fqdn",
        value="bad.com",
        parent_analysis=submission.root_analysis,
        analysis_tags=["analysis_tag1"],
        critical_points=["critical_point1"],
        directives=["directive1"],
        display_type="display_type1",
        time=time1,
        db=db,
    )
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", db=db)
    analysis = factory.analysis.create_or_read(
        analysis_module_type=analysis_module_type, submission=submission, target=observable1, db=db
    )
    factory.observable.create_or_read(
        type="fqdn", value="bad.com", parent_analysis=analysis, analysis_tags=["analysis_tag2"], db=db
    )
    factory.observable.create_or_read(
        type="ipv4",
        value="127.0.0.1",
        parent_analysis=submission.root_analysis,
        analysis_tags=["analysis_tag3"],
        display_value="display_value1",
        tags=["tag1"],
        db=db,
    )

    # Create a second submission tree with a duplicate observable from the first submission
    #
    # submission
    #   o2 - tag1, other_display_value
    #   o3
    submission2 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="ipv4",
        value="127.0.0.1",
        parent_analysis=submission2.root_analysis,
        display_value="other_display_value",
        db=db,
    )
    factory.observable.create_or_read(
        type="email_address", value="badguy@bad.com", parent_analysis=submission2.root_analysis, db=db
    )

    # Create a third submission tree that should not be included in the results
    #
    # submission
    #   o4 - analysis_tag4
    submission3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="ipv4",
        value="192.168.1.1",
        parent_analysis=submission3.root_analysis,
        analysis_tags=["analysis_tag4"],
        db=db,
    )

    # Fetching the list of observables in the submissions should only show three observables since
    # there were duplicates. The analysis tags are injected, and the observalbes should be sorted
    # by the types then values.
    #
    # email_address: badguy@bad.com (no permanent or analysis tags)
    # fqdn: bad.com (analysis_tag1, analysis_tag2)
    # ipv4: 127.0.0.1 (analysis_tag3, tag1)
    result = crud.submission.read_observables(uuids=[submission.uuid, submission2.uuid], db=db)
    assert len(result) == 3

    assert result[0].type.value == "email_address" and result[0].value == "badguy@bad.com"
    assert result[0].analysis_metadata.tags == []
    assert result[0].analysis_metadata.directives == []
    assert result[0].analysis_metadata.display_type is None
    assert result[0].analysis_metadata.display_value is None
    assert result[0].analysis_metadata.time is None
    assert result[0].tags == []

    assert result[1].type.value == "fqdn" and result[1].value == "bad.com"
    assert [c.value for c in result[1].analysis_metadata.critical_points] == ["critical_point1"]
    assert [d.value for d in result[1].analysis_metadata.directives] == ["directive1"]
    assert [t.value for t in result[1].analysis_metadata.tags] == ["analysis_tag1", "analysis_tag2"]
    assert result[1].analysis_metadata.display_type.value == "display_type1"
    assert result[1].analysis_metadata.display_value is None
    assert result[1].analysis_metadata.time.value == time1
    assert result[1].tags == []

    assert result[2].type.value == "ipv4" and result[2].value == "127.0.0.1"
    assert result[2].analysis_metadata.directives == []
    assert [t.value for t in result[2].analysis_metadata.tags] == ["analysis_tag3"]
    assert result[2].analysis_metadata.display_type is None
    assert result[2].analysis_metadata.display_value.value == "display_value1"
    assert result[0].analysis_metadata.time is None
    assert [t.value for t in result[2].tags] == ["tag1"]


def test_read_submission_tree(db):
    submission = factory.submission.create_from_json_file(
        db=db, json_path="/app/tests/alerts/small.json", submission_name="Test Alert"
    )

    # The small.json submission has 13 observables (12 unique) and 15 analyses. The small.json template actually shows
    # 14 observables and 15 analyses, but one of each of them are repeated, so they will actually only appear once
    # in the SubmissionTreeRead object.
    tree = crud.submission.read_tree(uuid=submission.uuid, db=db)
    tree_json = str(tree.dict())
    assert tree_json.count("'object_type': 'observable'") == 13
    assert tree_json.count("'object_type': 'analysis'") == 15
    assert len(tree.root_analysis.children) == 2
    assert tree.number_of_observables == 12

    # The small.json has three different analysis tags applied to observables, and they should be in alphabetical order.
    assert len(submission.child_analysis_tags) == 3
    assert submission.child_analysis_tags[0].value == "contacted_host"
    assert submission.child_analysis_tags[1].value == "from_address"
    assert submission.child_analysis_tags[2].value == "recipient"

    # The small.json has one detection point
    assert len(submission.child_detection_points) == 1
    assert submission.child_detection_points[0].value == "Malicious email address"

    # The small.json has one permanent tag applied to an observable.
    assert len(submission.child_tags) == 1
    assert submission.child_tags[0].value == "c2"


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
    #   o3 - url - https://example.com/index.html
    #   o4 - url - https://example3.com
    #   o5 - ipv4 - 1.2.3.4
    #   o6 - email_address - name@company.com

    factory.observable.create_or_read(
        type="url", value="https://example.com", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example2.com", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example.com/index.html", parent_analysis=submission1.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example3.com", parent_analysis=submission1.root_analysis, db=db
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


def test_tag_functionality(db):
    """
    Submission1
        RootAnalysis1
            O1 - tag1
                A1 - adds tag z_analysis1_tag to O2
                    O2 - analysis2_tag, z_analysis1_tag (should show all analysis tags in this alert for the observable)
            O3
                A2 - adds tag analysis2_tag to O2
                    O2 - analysis2_tag, z_analysis1_tag (should show all analysis tags in this alert for the observable)

    Submission2
        RootAnalysis2
            O1 - should have tag1 because it is a permanent tag
            O2 - should not have any tags because the alert does not contain analysis A1 or A2
    """

    # Create the submission1 tree structure
    submission1 = factory.submission.create(db=db)

    sub1_o1 = factory.observable.create_or_read(
        type="type1",
        value="value1",
        parent_analysis=submission1.root_analysis,
        tags=["tag1"],
        db=db,
    )

    amt1 = factory.analysis_module_type.create_or_read(value="amt1", db=db)
    o1_a1 = factory.analysis.create_or_read(analysis_module_type=amt1, submission=submission1, target=sub1_o1, db=db)

    a1_o2 = factory.observable.create_or_read(
        type="type2", value="value2", parent_analysis=o1_a1, analysis_tags=["z_analysis1_tag"], db=db
    )

    sub1_o3 = factory.observable.create_or_read(
        type="type3", value="value3", parent_analysis=submission1.root_analysis, db=db
    )

    amt2 = factory.analysis_module_type.create_or_read(value="amt2", db=db)
    o3_a2 = factory.analysis.create_or_read(analysis_module_type=amt2, submission=submission1, target=sub1_o3, db=db)

    a2_o2 = factory.observable.create_or_read(
        type="type2", value="value2", parent_analysis=o3_a2, analysis_tags=["analysis2_tag"], db=db
    )

    # Create the submission2 tree structure
    submission2 = factory.submission.create(db=db)

    sub2_o1 = factory.observable.create_or_read(
        type="type1", value="value1", parent_analysis=submission2.root_analysis, db=db
    )

    sub2_o2 = factory.observable.create_or_read(
        type="type2", value="value2", parent_analysis=submission2.root_analysis, db=db
    )

    # Verify the tag relationships on the submissions
    assert [t.value for t in submission1.child_analysis_tags] == ["analysis2_tag", "z_analysis1_tag"]
    assert [t.value for t in submission1.child_tags] == ["tag1"]

    assert submission2.child_analysis_tags == []
    assert [t.value for t in submission2.child_tags] == ["tag1"]

    # The two instances of O1 across both submissions should be the same observable
    assert sub1_o1.uuid == sub2_o1.uuid

    # The two instances of O1 should both have the tag1 tag
    assert len(sub1_o1.tags) == 1
    assert sub1_o1.tags[0].value == "tag1"
    assert len(sub2_o1.tags) == 1
    assert sub2_o1.tags[0].value == "tag1"

    # The three instances of O2 across both submissions should be the same observable
    assert a1_o2.uuid == a2_o2.uuid == sub2_o2.uuid

    # The analysis tags are only associated with their observables when the submission tree is constructed
    submission1_tree = crud.submission.read_tree(submission1.uuid, db=db)
    submission2_tree = crud.submission.read_tree(submission2.uuid, db=db)

    # The first submission should have two child observables, and they should be in the order
    # in which they were added to the tree (they are not sorted).
    assert len(submission1_tree.root_analysis.children) == 2
    assert submission1_tree.root_analysis.children[0].uuid == sub1_o1.uuid
    assert submission1_tree.root_analysis.children[1].uuid == sub1_o3.uuid

    # Verify the tags for O1 in the first submission
    assert len(submission1_tree.root_analysis.children[0].tags) == 1
    assert submission1_tree.root_analysis.children[0].tags[0].value == "tag1"

    # Verify the tags for O2 in the first submission under A1. It should have two tags, even though
    # its parent analysis A1 only added one tag. The tags should be in alphabetical order, not the
    # order in which they were added by the analyses.
    assert len(submission1_tree.root_analysis.children[0].children[0].children[0].analysis_metadata.tags) == 2
    assert (
        submission1_tree.root_analysis.children[0].children[0].children[0].analysis_metadata.tags[0].value
        == "analysis2_tag"
    )
    assert (
        submission1_tree.root_analysis.children[0].children[0].children[0].analysis_metadata.tags[1].value
        == "z_analysis1_tag"
    )

    # Verify the tags for O2 in the first submission under A2. It should have two tags, even though
    # its parent analysis A2 only added one tag. The tags should be in alphabetical order, not the
    # order in which they were added by the analyses.
    assert len(submission1_tree.root_analysis.children[1].children[0].children[0].analysis_metadata.tags) == 2
    assert (
        submission1_tree.root_analysis.children[1].children[0].children[0].analysis_metadata.tags[0].value
        == "analysis2_tag"
    )
    assert (
        submission1_tree.root_analysis.children[1].children[0].children[0].analysis_metadata.tags[1].value
        == "z_analysis1_tag"
    )

    # The second submission should have two child observables, and they should be in the order
    # in which they were added to the tree (they are not sorted).
    assert len(submission2_tree.root_analysis.children) == 2
    assert submission2_tree.root_analysis.children[0].uuid == sub2_o1.uuid
    assert submission2_tree.root_analysis.children[1].uuid == sub2_o2.uuid

    # Verify the tags for O1 in the second submission
    assert len(submission2_tree.root_analysis.children[0].tags) == 1
    assert submission2_tree.root_analysis.children[0].tags[0].value == "tag1"

    # Verify the tags for O2 in the second submission. Even though it is the exact same observable
    # object as in the first submission, it shouldn't have any tags because the submission does not
    # contain any analysis that added tags to it.
    assert submission2_tree.root_analysis.children[1].analysis_metadata.tags == []
    assert submission2_tree.root_analysis.children[1].tags == []


def test_child_observables(db):
    """
    Submission1
        O1
            A1
                O2
        O3
            A2
                O2

    Submission2
        O1
        O4
    """

    # Create the submission1 tree structure
    submission1 = factory.submission.create(db=db)

    sub1_o1 = factory.observable.create_or_read(
        type="type1",
        value="value1",
        parent_analysis=submission1.root_analysis,
        db=db,
    )

    amt1 = factory.analysis_module_type.create_or_read(value="amt1", db=db)
    o1_a1 = factory.analysis.create_or_read(analysis_module_type=amt1, submission=submission1, target=sub1_o1, db=db)

    a1_o2 = factory.observable.create_or_read(type="type2", value="value2", parent_analysis=o1_a1, db=db)

    sub1_o3 = factory.observable.create_or_read(
        type="type3", value="value3", parent_analysis=submission1.root_analysis, db=db
    )

    amt2 = factory.analysis_module_type.create_or_read(value="amt2", db=db)
    o3_a2 = factory.analysis.create_or_read(analysis_module_type=amt2, submission=submission1, target=sub1_o3, db=db)

    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=o3_a2, db=db)

    # Create the submission2 tree structure
    submission2 = factory.submission.create(db=db)

    sub2_o1 = factory.observable.create_or_read(
        type="type1", value="value1", parent_analysis=submission2.root_analysis, db=db
    )

    sub2_o4 = factory.observable.create_or_read(
        type="type4", value="value4", parent_analysis=submission2.root_analysis, db=db
    )

    # Verify the child_observables on submission1 - there should be 3 - O1, O2, O3
    assert len(submission1.child_observables) == 3
    assert sub1_o1 in submission1.child_observables
    assert a1_o2 in submission1.child_observables
    assert sub1_o3 in submission1.child_observables

    # Verify the child_observables on submission2 - there should be 2 - O1, O4
    assert len(submission2.child_observables) == 2
    assert sub2_o1 in submission2.child_observables
    assert sub2_o4 in submission2.child_observables


def test_disposition_history(db):
    # Create some alert dispositions
    factory.alert_disposition.create_or_read(value="FALSE_POSITIVE", rank=1, db=db)
    factory.alert_disposition.create_or_read(value="DELIVERY", rank=2, db=db)

    # Create four alerts that all have the same observable but different dispositions
    submission1 = factory.submission.create(alert=True, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission1.root_analysis, db=db)

    submission2 = factory.submission.create(alert=True, disposition="FALSE_POSITIVE", db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission2.root_analysis, db=db)

    submission3 = factory.submission.create(alert=True, disposition="FALSE_POSITIVE", db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission3.root_analysis, db=db)

    submission4 = factory.submission.create(alert=True, disposition="DELIVERY", db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission4.root_analysis, db=db)

    # Read one of the alert trees
    tree = crud.submission.read_tree(uuid=submission1.uuid, db=db)

    # The disposition history for the observable should be sorted by the dispositions' ranks.
    assert len(tree.root_analysis.children[0].disposition_history) == 3
    assert tree.root_analysis.children[0].disposition_history[0].disposition == "FALSE_POSITIVE"
    assert tree.root_analysis.children[0].disposition_history[0].count == 2
    assert tree.root_analysis.children[0].disposition_history[0].percent == 50

    assert tree.root_analysis.children[0].disposition_history[1].disposition == "DELIVERY"
    assert tree.root_analysis.children[0].disposition_history[1].count == 1
    assert tree.root_analysis.children[0].disposition_history[1].percent == 25

    assert tree.root_analysis.children[0].disposition_history[2].disposition == "OPEN"
    assert tree.root_analysis.children[0].disposition_history[2].count == 1
    assert tree.root_analysis.children[0].disposition_history[2].percent == 25

    # Similarly, if you read the observables from a set of alerts instead, you should get the same disposition history.
    observables = crud.submission.read_observables(uuids=[submission1.uuid], db=db)
    assert len(observables) == 1
    assert len(observables[0].disposition_history) == 3
    assert observables[0].disposition_history[0].disposition == "FALSE_POSITIVE"
    assert observables[0].disposition_history[0].count == 2
    assert observables[0].disposition_history[0].percent == 50

    assert observables[0].disposition_history[1].disposition == "DELIVERY"
    assert observables[0].disposition_history[1].count == 1
    assert observables[0].disposition_history[1].percent == 25

    assert observables[0].disposition_history[2].disposition == "OPEN"
    assert observables[0].disposition_history[2].count == 1
    assert observables[0].disposition_history[2].percent == 25


def test_observable_matching_events(db):
    # Create some event statuses
    factory.event_status.create_or_read(value="OPEN", db=db)
    factory.event_status.create_or_read(value="CLOSED", db=db)

    # Create some events that all contain the same observable but have different statuses
    event1 = factory.event.create_or_read(name="event1", status="OPEN", db=db)
    submission1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission1.root_analysis, db=db)

    event2 = factory.event.create_or_read(name="event2", status="OPEN", db=db)
    submission2 = factory.submission.create(event=event2, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission2.root_analysis, db=db)

    event3 = factory.event.create_or_read(name="event3", status="CLOSED", db=db)
    submission3 = factory.submission.create(event=event3, db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission3.root_analysis, db=db)

    # Create another event that does not contain the same observable - this should not appear in the results.
    event4 = factory.event.create_or_read(name="event4", status="CLOSED", db=db)
    submission4 = factory.submission.create(event=event4, db=db)
    factory.observable.create_or_read(type="type4", value="value4", parent_analysis=submission4.root_analysis, db=db)

    # Read one of the alert trees
    tree = crud.submission.read_tree(uuid=submission1.uuid, db=db)

    # The matching event information for the observable should be sorted by the status' values.
    assert len(tree.root_analysis.children[0].matching_events) == 2
    assert tree.root_analysis.children[0].matching_events[0].status == "CLOSED"
    assert tree.root_analysis.children[0].matching_events[0].count == 1
    assert tree.root_analysis.children[0].matching_events[1].status == "OPEN"
    assert tree.root_analysis.children[0].matching_events[1].count == 2

    # Similarly, if you read the observables from a set of alerts instead, you should get the same matching event information.
    observables = crud.submission.read_observables(uuids=[submission1.uuid], db=db)
    assert len(observables) == 1
    assert len(observables[0].matching_events) == 2
    assert observables[0].matching_events[0].status == "CLOSED"
    assert observables[0].matching_events[0].count == 1
    assert observables[0].matching_events[1].status == "OPEN"
    assert observables[0].matching_events[1].count == 2


def test_submission_matching_events(db):
    """
    Submission1
        O1
        O2
        O3
    """

    # Create a submission with a few observables
    submission1 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="type1", value="value1", parent_analysis=submission1.root_analysis, tags=["o1_tag"], db=db
    )
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=submission1.root_analysis, db=db)
    factory.observable.create_or_read(type="type3", value="value3", parent_analysis=submission1.root_analysis, db=db)

    """
    Event1 - OPEN
        O1
        O2
        O3

    Event2 - CLOSED
        O2
        O3

    Event3 - IGNORE
        O3

    Event4 - This event should not appear in the results
        O4
    """
    # Create some events that all contain the same observable
    event1 = factory.event.create_or_read(name="event1", status="OPEN", db=db)
    submission2 = factory.submission.create(event=event1, tags=["submission2_tag"], db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission2.root_analysis, db=db)
    factory.observable.create_or_read(
        type="type2",
        value="value2",
        parent_analysis=submission2.root_analysis,
        analysis_tags=["o2_analysis_tag"],
        db=db,
    )
    factory.observable.create_or_read(type="type3", value="value3", parent_analysis=submission2.root_analysis, db=db)

    event2 = factory.event.create_or_read(name="event2", status="CLOSED", db=db)
    submission3 = factory.submission.create(event=event2, db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=submission3.root_analysis, db=db)
    factory.observable.create_or_read(type="type3", value="value3", parent_analysis=submission3.root_analysis, db=db)

    event3 = factory.event.create_or_read(name="event3", status="IGNORE", db=db)
    submission4 = factory.submission.create(event=event3, db=db)
    factory.observable.create_or_read(type="type3", value="value3", parent_analysis=submission4.root_analysis, db=db)

    # Create another event that does not contain any of the same observables - this should not appear in the results.
    event4 = factory.event.create_or_read(name="event4", db=db)
    submission5 = factory.submission.create(event=event4, db=db)
    factory.observable.create_or_read(type="type4", value="value4", parent_analysis=submission5.root_analysis, db=db)

    # Read one of the alert trees
    tree = crud.submission.read_tree(uuid=submission1.uuid, db=db)

    # Verify the matching events
    assert len(tree.matching_events) == 3

    assert tree.matching_events[0].status == "OPEN"
    assert len(tree.matching_events[0].events) == 1
    assert tree.matching_events[0].events[0].count == 3
    assert tree.matching_events[0].events[0].percent == 100
    assert tree.matching_events[0].events[0].event.name == "event1"
    assert len(tree.matching_events[0].events[0].event.all_tags) == 3

    assert tree.matching_events[1].status == "CLOSED"
    assert len(tree.matching_events[1].events) == 1
    assert tree.matching_events[1].events[0].count == 2
    assert tree.matching_events[1].events[0].percent == 66
    assert tree.matching_events[1].events[0].event.name == "event2"
    assert len(tree.matching_events[1].events[0].event.all_tags) == 0

    assert tree.matching_events[2].status == "IGNORE"
    assert len(tree.matching_events[2].events) == 1
    assert tree.matching_events[2].events[0].count == 1
    assert tree.matching_events[2].events[0].percent == 33
    assert tree.matching_events[2].events[0].event.name == "event3"
    assert len(tree.matching_events[2].events[0].event.all_tags) == 0


def test_observable_sort_order(db):
    """
    Create a submission with the following structure:

    Submission
        O1 - no sort
        O2 - no sort
            A1
                O3 - no sort
                O4 - no sort
    """

    submission = factory.submission.create(db=db)
    factory.observable.create_or_read(type="type1", value="value1", parent_analysis=submission.root_analysis, db=db)
    o2 = factory.observable.create_or_read(
        type="type2", value="value2", parent_analysis=submission.root_analysis, db=db
    )
    a1 = factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="test_module", db=db),
        submission=submission,
        target=o2,
        db=db,
    )
    factory.observable.create_or_read(type="type3", value="value3", parent_analysis=a1, db=db)
    factory.observable.create_or_read(type="type4", value="value4", parent_analysis=a1, db=db)

    # Verify the order of the observables in the tree. They will appear in the order in which they were added.
    tree = crud.submission.read_tree(uuid=submission.uuid, db=db)
    assert tree.root_analysis.children[0].type.value == "type1" and tree.root_analysis.children[0].value == "value1"
    assert tree.root_analysis.children[1].type.value == "type2" and tree.root_analysis.children[1].value == "value2"
    assert (
        tree.root_analysis.children[1].children[0].children[0].type.value == "type3"
        and tree.root_analysis.children[1].children[0].children[0].value == "value3"
    )
    assert (
        tree.root_analysis.children[1].children[0].children[1].type.value == "type4"
        and tree.root_analysis.children[1].children[0].children[1].value == "value4"
    )

    """
    Then add two observables to it that specify a sort order:

    Submission
        O5 - sort 1
        O1 - no sort
        O2 - no sort
            A1
                O6 - sort 1
                O3 - no sort
                O4 - no sort
    """

    factory.observable.create_or_read(
        type="type5", value="value5", parent_analysis=submission.root_analysis, sort=1, db=db
    )
    factory.observable.create_or_read(type="type6", value="value6", parent_analysis=a1, sort=1, db=db)

    # Verify the order of the observables in the tree now that it has some observables with a sort applied.
    tree = crud.submission.read_tree(uuid=submission.uuid, db=db)
    assert tree.root_analysis.children[0].type.value == "type5" and tree.root_analysis.children[0].value == "value5"
    assert tree.root_analysis.children[1].type.value == "type1" and tree.root_analysis.children[1].value == "value1"
    assert tree.root_analysis.children[2].type.value == "type2" and tree.root_analysis.children[2].value == "value2"
    assert (
        tree.root_analysis.children[2].children[0].children[0].type.value == "type6"
        and tree.root_analysis.children[2].children[0].children[0].value == "value6"
    )
    assert (
        tree.root_analysis.children[2].children[0].children[1].type.value == "type3"
        and tree.root_analysis.children[2].children[0].children[1].value == "value3"
    )
    assert (
        tree.root_analysis.children[2].children[0].children[2].type.value == "type4"
        and tree.root_analysis.children[2].children[0].children[2].value == "value4"
    )


def test_circular_tree(db):
    """
    The circular test alert has a structure like:

    RootAnalysis
        fqdn: evil.com
            Domain Analysis
                ipv4: 127.0.0.1
                    IP Analysis
                        fqdn: evil.com <-- cut off the loop here
    """

    submission = factory.submission.create_from_json_file(
        db=db, json_path="/app/tests/alerts/circular.json", submission_name="Circular Alert"
    )

    tree = crud.submission.read_tree(uuid=submission.uuid, db=db)
    assert len(tree.root_analysis.children) == 1

    # Verify the first evil.com
    assert tree.root_analysis.children[0].type.value == "fqdn" and tree.root_analysis.children[0].value == "evil.com"
    assert tree.root_analysis.children[0].jump_to_leaf is None
    assert tree.root_analysis.children[0].leaf_id == f"{tree.root_analysis.children[0].uuid}-0"
    assert len(tree.root_analysis.children[0].children) == 1

    # Verify the Domain Analysis
    assert tree.root_analysis.children[0].children[0].analysis_module_type.value == "Domain Analysis"
    assert tree.root_analysis.children[0].children[0].leaf_id == f"{tree.root_analysis.children[0].children[0].uuid}"
    assert len(tree.root_analysis.children[0].children[0].children) == 1

    # Verify the ipv4 observable
    assert (
        tree.root_analysis.children[0].children[0].children[0].type.value == "ipv4"
        and tree.root_analysis.children[0].children[0].children[0].value == "127.0.0.1"
    )
    assert tree.root_analysis.children[0].children[0].children[0].jump_to_leaf is None
    assert (
        tree.root_analysis.children[0].children[0].children[0].leaf_id
        == f"{tree.root_analysis.children[0].children[0].children[0].uuid}-0"
    )
    assert len(tree.root_analysis.children[0].children[0].children[0].children) == 1

    # Verify the IP Analysis
    assert (
        tree.root_analysis.children[0].children[0].children[0].children[0].analysis_module_type.value == "IP Analysis"
    )
    assert (
        tree.root_analysis.children[0].children[0].children[0].children[0].leaf_id
        == f"{tree.root_analysis.children[0].children[0].children[0].children[0].uuid}"
    )
    assert len(tree.root_analysis.children[0].children[0].children[0].children[0].children) == 1

    # Verify the second evil.com
    assert (
        tree.root_analysis.children[0].children[0].children[0].children[0].children[0].type.value == "fqdn"
        and tree.root_analysis.children[0].children[0].children[0].children[0].children[0].value == "evil.com"
    )
    assert (
        tree.root_analysis.children[0].children[0].children[0].children[0].children[0].jump_to_leaf
        == tree.root_analysis.children[0].leaf_id
    )
    assert (
        tree.root_analysis.children[0].children[0].children[0].children[0].children[0].leaf_id
        == f"{tree.root_analysis.children[0].uuid}-1"
    )
    assert tree.root_analysis.children[0].children[0].children[0].children[0].children[0].children == []


def test_status(db):
    submission = factory.submission.create(db=db)
    obs = factory.observable.create_or_read(type="type", value="value", parent_analysis=submission.root_analysis, db=db)

    # Possible status combinations are:
    #
    # running -> running
    # ignore -> ignore
    # complete -> complete
    # complete, running -> running
    # complete, ignore -> complete
    # ignore, running -> running
    # complete, running, ignore -> running

    # Test with all the same status
    a1 = factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="test_module1", db=db),
        status="complete",
        submission=submission,
        target=obs,
        db=db,
    )

    a2 = factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="test_module2", db=db),
        status="complete",
        submission=submission,
        target=obs,
        db=db,
    )

    a3 = factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="test_module3", db=db),
        status="complete",
        submission=submission,
        target=obs,
        db=db,
    )

    assert submission.status.value == "complete"

    # Test with complete and running
    a1.status = factory.analysis_status.create_or_read(value="running", db=db)
    a2.status = factory.analysis_status.create_or_read(value="complete", db=db)
    a3.status = factory.analysis_status.create_or_read(value="complete", db=db)
    db.refresh(submission)

    assert submission.status.value == "running"

    # Test with complete and ignore
    a1.status = factory.analysis_status.create_or_read(value="ignore", db=db)
    a2.status = factory.analysis_status.create_or_read(value="complete", db=db)
    a3.status = factory.analysis_status.create_or_read(value="complete", db=db)
    db.refresh(submission)

    assert submission.status.value == "complete"

    # Test with running and ignore
    a1.status = factory.analysis_status.create_or_read(value="ignore", db=db)
    a2.status = factory.analysis_status.create_or_read(value="running", db=db)
    a3.status = factory.analysis_status.create_or_read(value="running", db=db)
    db.refresh(submission)

    assert submission.status.value == "running"

    # Test with all three statuses
    a1.status = factory.analysis_status.create_or_read(value="complete", db=db)
    a2.status = factory.analysis_status.create_or_read(value="ignore", db=db)
    a3.status = factory.analysis_status.create_or_read(value="running", db=db)
    db.refresh(submission)

    assert submission.status.value == "running"


def test_critical_path(db):
    """
    * - critical path
    (*) - critical point

    RootAnalysis
        obs_type1: value1
            Analysis 1
                obs_type3: value3
        obs_type2: value2 *
            Analysis 2 *
                obs_type4: value4 (*)
                    Analysis 3
                        obs_type5: value5

    """

    submission = factory.submission.create_from_json_file(
        db=db, json_path="/app/tests/alerts/critical_path.json", submission_name="Critical Path Alert"
    )

    tree = crud.submission.read_tree(uuid=submission.uuid, db=db)
    assert len(tree.root_analysis.children) == 2

    # Verify obs_type1: value1
    assert tree.root_analysis.children[0].type.value == "obs_type1" and tree.root_analysis.children[0].value == "value1"
    assert tree.root_analysis.children[0].critical_path is False
    assert len(tree.root_analysis.children[0].children) == 1

    # Verify analysis1
    assert tree.root_analysis.children[0].children[0].analysis_module_type.value == "Analysis 1"
    assert tree.root_analysis.children[0].children[0].critical_path is False
    assert len(tree.root_analysis.children[0].children[0].children) == 1

    # Verify obs_type3: value3
    assert (
        tree.root_analysis.children[0].children[0].children[0].type.value == "obs_type3"
        and tree.root_analysis.children[0].children[0].children[0].value == "value3"
    )
    assert tree.root_analysis.children[0].children[0].children[0].critical_path is False
    assert len(tree.root_analysis.children[0].children[0].children[0].children) == 0

    # Verify obs_type2: value2
    assert tree.root_analysis.children[1].type.value == "obs_type2" and tree.root_analysis.children[1].value == "value2"
    assert tree.root_analysis.children[1].critical_path is True
    assert len(tree.root_analysis.children[1].children) == 1

    # Verify analysis2
    assert tree.root_analysis.children[1].children[0].analysis_module_type.value == "Analysis 2"
    assert tree.root_analysis.children[1].children[0].critical_path is True
    assert len(tree.root_analysis.children[1].children[0].children) == 1

    # Verify obs_type4: value4
    assert (
        tree.root_analysis.children[1].children[0].children[0].type.value == "obs_type4"
        and tree.root_analysis.children[1].children[0].children[0].value == "value4"
    )
    assert tree.root_analysis.children[1].children[0].children[0].critical_path is True
    assert len(tree.root_analysis.children[1].children[0].children[0].children) == 1

    # Verify analysis3
    assert tree.root_analysis.children[1].children[0].children[0].children[0].analysis_module_type.value == "Analysis 3"
    assert tree.root_analysis.children[1].children[0].children[0].children[0].critical_path is False
    assert len(tree.root_analysis.children[1].children[0].children[0].children[0].children) == 1

    # Verify obs_type5: value5
    assert (
        tree.root_analysis.children[1].children[0].children[0].children[0].children[0].type.value == "obs_type5"
        and tree.root_analysis.children[1].children[0].children[0].children[0].children[0].value == "value5"
    )
    assert tree.root_analysis.children[1].children[0].children[0].children[0].children[0].critical_path is False
    assert len(tree.root_analysis.children[1].children[0].children[0].children[0].children[0].children) == 0
