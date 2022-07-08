import pytest
import uuid

from datetime import timedelta
from fastapi import status
from urllib.parse import urlencode

from db import crud
from tests import factory


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/submission/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/submission/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "path",
    [
        ("/summary/url_domain"),
    ],
)
def test_get_summary_nonexistent_submission(client, path):
    get = client.get(f"/api/submission/{uuid.uuid4()}{path}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_get_version_nonexistent_uuid(client):
    get = client.get(f"/api/submission/{uuid.uuid4()}/version")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_version(client, db):
    submission = factory.submission.create(db=db)

    get = client.get(f"/api/submission/{submission.uuid}/version")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {"version": str(submission.version)}


def test_get_all_pagination(client, db):
    # Create 11 submissions
    for _ in range(11):
        factory.submission.create(db=db)

    # Keep track of all of the submission UUIDs to make sure we read them all
    unique_submission_uuids = set()

    # Read every page in chunks of 2 while there are still results
    offset = 0
    while True:
        get = client.get(f"/api/submission/?limit=2&offset={offset}")

        # Store the submission UUIDs
        for submission in get.json()["items"]:
            unique_submission_uuids.add(submission["uuid"])

            # Make sure the object_type field is "submission"
            assert submission["object_type"] == "submission"

        # Check if there is another page to retrieve
        if len(unique_submission_uuids) < get.json()["total"]:
            # Increase the offset to get the next page
            offset += get.json()["limit"]
            continue

        break

    # Should have gotten all 11 submissions across the pages
    assert len(unique_submission_uuids) == 11


def test_get_all_empty(client):
    get = client.get("/api/submission/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {"items": [], "limit": 50, "offset": 0, "total": 0}


def test_get_filter_alert(client, db):
    # Create some submissions where only one of them is marked as being an alert
    #
    # submission1 - alert
    #
    # submission2
    submission1 = factory.submission.create(alert=True, db=db)
    factory.submission.create(db=db)

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by alert=true
    get = client.get("/api/submission/?alert=true")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)


def test_get_filter_disposition(client, db):
    factory.submission.create(db=db)
    submission1 = factory.submission.create(db=db, disposition="FALSE_POSITIVE")
    submission2 = factory.submission.create(db=db, disposition="UNKNOWN")

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should only be 1 submission when we filter by the disposition
    get = client.get("/api/submission/?disposition=FALSE_POSITIVE")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["disposition"]["value"] == "FALSE_POSITIVE"

    # There should only be 1 submission when we filter by none
    get = client.get("/api/submission/?disposition=none")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["disposition"] is None

    # There should be 2 submissions when we filter by FALSE_POSITIVE and UNKNOWN
    get = client.get("/api/submission/?disposition=FALSE_POSITIVE&disposition=UNKNOWN")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])


def test_get_filter_disposition_user(client, db):
    factory.submission.create(db=db, history_username="analyst")
    submission = factory.submission.create(
        db=db, disposition="FALSE_POSITIVE", updated_by_user="analyst", history_username="analyst"
    )

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by the disposition user
    get = client.get("/api/submission/?disposition_user=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission.uuid)


def test_get_filter_disposition_user_multiple(client, db):
    factory.submission.create(db=db, history_username="analyst")

    # This submission was first dispositioned by alice
    submission2 = factory.submission.create(
        db=db, disposition="FALSE_POSITIVE", updated_by_user="alice", history_username="alice"
    )

    # This submission was first dispositioned by analyst
    submission3 = factory.submission.create(
        db=db, disposition="FALSE_POSITIVE", updated_by_user="analyst", history_username="analyst"
    )

    # analyst re-dispositions alice's submission
    factory.alert_disposition.create_or_read(value="DELIVERY", rank=2, db=db)
    update = client.patch(
        "/api/submission/",
        json=[{"disposition": "DELIVERY", "history_username": "analyst", "uuid": str(submission2.uuid)}],
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the submission is no longer dispositioned by alice
    get = client.get(f"/api/submission/{submission2.uuid}")
    assert get.json()["disposition_user"]["username"] == "analyst"

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should still be 1 submission when we filter by the disposition user alice
    get = client.get("/api/submission/?disposition_user=alice")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)

    # There should be 3 submissions when we filter by the disposition user analyst and alice
    get = client.get("/api/submission/?disposition_user=alice&disposition_user=analyst")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission3.uuid) for a in get.json()["items"])


def test_get_filter_dispositioned_after(client, db):
    now = crud.helpers.utcnow()
    factory.submission.create(db=db, history_username="analyst")
    factory.submission.create(db=db, disposition="FALSE_POSITIVE", update_time=now, history_username="analyst")
    factory.submission.create(
        db=db, disposition="FALSE_POSITIVE", update_time=now + timedelta(seconds=5), history_username="analyst"
    )

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should only be 1 submission when we filter by dispositioned_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"dispositioned_after": now}
    get = client.get(f"/api/submission/?{urlencode(params1)}")
    assert get.json()["total"] == 1

    # There should be 2 submissions when we filter by two dispositioned_after values
    params2 = {"dispositioned_after": now - timedelta(seconds=5)}
    get = client.get(f"/api/submission/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2


def test_get_filter_dispositioned_before(client, db):
    now = crud.helpers.utcnow()
    factory.submission.create(db=db, history_username="analyst")
    factory.submission.create(
        db=db, disposition="FALSE_POSITIVE", update_time=now - timedelta(seconds=5), history_username="analyst"
    )
    factory.submission.create(db=db, disposition="FALSE_POSITIVE", update_time=now, history_username="analyst")

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should only be 1 submission when we filter by dispositioned_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"dispositioned_before": now}
    get = client.get(f"/api/submission/?{urlencode(params1)}")
    assert get.json()["total"] == 1

    # There should be 2 submissions when we filter by two dispositioned_before values
    params2 = {"dispositioned_before": now + timedelta(seconds=6)}
    get = client.get(f"/api/submission/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2


def test_get_filter_dispositioned_after_and_before(client, db):
    now = crud.helpers.utcnow()
    after = now - timedelta(days=1)
    before = now + timedelta(days=1)
    factory.submission.create(db=db, disposition="FALSE_POSITIVE", update_time=after, history_username="analyst")
    factory.submission.create(db=db, disposition="FALSE_POSITIVE", update_time=now, history_username="analyst")
    factory.submission.create(db=db, disposition="FALSE_POSITIVE", update_time=before, history_username="analyst")

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should only be 1 submission when we filter by dispositioned_after and dispositioned_before.
    # But the timestamp has a timezone specified, which uses the + symbol that needs to be
    # urlencoded since it is a reserved URL character.
    params = {
        "dispositioned_after": after,
        "dispositioned_before": before,
    }
    get = client.get(f"/api/submission/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_after(client, db):
    now = crud.helpers.utcnow()
    submission = factory.submission.create(db=db, event_time=now)
    factory.submission.create(db=db, event_time=now + timedelta(seconds=5))

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by event_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"event_time_after": submission.event_time}
    get = client.get(f"/api/submission/?{urlencode(params1)}")
    assert get.json()["total"] == 1

    # There should be 2 submissions when we filter by multiple event_time_after
    params2 = {"event_time_after": now - timedelta(seconds=5)}
    get = client.get(f"/api/submission/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2


def test_get_filter_event_time_before(client, db):
    now = crud.helpers.utcnow()
    factory.submission.create(db=db, event_time=now)
    submission = factory.submission.create(db=db, event_time=now + timedelta(seconds=5))

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by event_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"event_time_before": submission.event_time}
    get = client.get(f"/api/submission/?{urlencode(params1)}")
    assert get.json()["total"] == 1

    # There should be 2 submissions when we filter by multiple event_time_after
    params2 = {"event_time_before": now + timedelta(seconds=6)}
    get = client.get(f"/api/submission/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2


def test_get_filter_event_uuid(client, db):
    # Create an event
    event1 = factory.event.create_or_read(name="Test Event", db=db)
    event2 = factory.event.create_or_read(name="Test Event 2", db=db)

    # Create some submissions
    factory.submission.create(db=db)
    submission1 = factory.submission.create(db=db, event=event1)
    submission2 = factory.submission.create(db=db, event=event2)

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should only be 1 submission when we filter by the event_uuid
    get = client.get(f"/api/submission/?event_uuid={event1.uuid}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][0]["event_uuid"] == str(event1.uuid)

    # There be 2 submissions when we filter by 2 event_uuids
    get = client.get(f"/api/submission/?event_uuid={event1.uuid}&event_uuid={event2.uuid}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])


def test_get_filter_insert_time_after(client, db):
    now = crud.helpers.utcnow()
    submission = factory.submission.create(db=db, insert_time=now)
    factory.submission.create(db=db, insert_time=now + timedelta(seconds=5))

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by insert_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"insert_time_after": submission.insert_time}
    get = client.get(f"/api/submission/?{urlencode(params1)}")
    assert get.json()["total"] == 1

    # There should be 2 submissions when we filter by multiple insert_time_after
    params2 = {"insert_time_after": now - timedelta(seconds=5)}
    get = client.get(f"/api/submission/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2


def test_get_filter_insert_time_before(client, db):
    now = crud.helpers.utcnow()
    factory.submission.create(db=db, insert_time=now - timedelta(seconds=5))
    submission = factory.submission.create(db=db, insert_time=now)

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by insert_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"insert_time_before": submission.insert_time}
    get = client.get(f"/api/submission/?{urlencode(params1)}")
    assert get.json()["total"] == 1

    # There should be 2 submissions when we filter by two insert_time_before values
    params2 = {"insert_time_before": now + timedelta(seconds=6)}
    get = client.get(f"/api/submission/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2


def test_get_filter_name(client, db):
    submission1 = factory.submission.create(db=db, name="Test Alert")
    submission2 = factory.submission.create(db=db, name="Some Other Alert")

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by the name
    get = client.get("/api/submission/?name=test alert")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "Test Alert"

    # There should be 2 submissions when we filter by two names
    get = client.get("/api/submission/?name=test alert&name=some other alert")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])


def test_get_filter_observable(client, db):
    # Create an empty submission
    factory.submission.create(db=db)

    # Create some submissions with one observable
    submission1 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission1.root_analysis, type="test_type1", value="test_value1", db=db
    )

    submission2 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission2.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # Create an submission with multiple observables
    submission3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission3.root_analysis, type="test_type1", value="test_value_asdf", db=db
    ),
    factory.observable.create_or_read(
        parent_analysis=submission3.root_analysis, type="test_type2", value="test_value1", db=db
    ),
    factory.observable.create_or_read(
        parent_analysis=submission3.root_analysis, type="test_type2", value="test_value2", db=db
    ),

    # There should be 4 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 4

    # There should only be 1 submission when we filter by the test_type1/test_value1 observable
    get = client.get("/api/submission/?observable=test_type1|test_value1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)

    # There should be 2 submissions when we filter by the test_type2/test_value2 observable
    get = client.get("/api/submission/?observable=test_type2|test_value2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission3.uuid) for a in get.json()["items"])

    # There should be 3 submissions when we filter by the test_type2/test_value2 observable and the test_type1/test_value1 observable
    get = client.get("/api/submission/?observable=test_type1|test_value1&observable=test_type2|test_value2")
    assert get.json()["total"] == 3
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission3.uuid) for a in get.json()["items"])


def test_get_filter_observable_types(client, db):
    # Create an empty submission
    factory.submission.create(db=db)

    # Create an submission with one observable
    submission1 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission1.root_analysis, type="test_type1", value="test_value1", db=db
    )

    # Create an submission with multiple observables
    submission2 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission2.root_analysis, type="test_type1", value="test_value_asdf", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=submission2.root_analysis, type="test_type2", value="test_value1", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=submission2.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should be 2 submissions when we filter by just test_type1
    get = client.get("/api/submission/?observable_types=test_type1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])

    # There should only be 1 submission when we filter by the test_type1 and test_type2
    get = client.get("/api/submission/?observable_types=test_type1,test_type2")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)

    # There should be 2 submissions when we filter by the test_type1 and test_type2 OR just test_type1
    get = client.get("/api/submission/?observable_types=test_type1,test_type2&observable_types=test_type1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])


def test_get_filter_observable_value(client, db):
    # Create an empty submission
    factory.submission.create(db=db)

    # Create some submissions with one observable
    submission1 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission1.root_analysis, type="test_type1", value="test_value1", db=db
    )

    submission2 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission2.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # Create an submission with multiple observables
    submission3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission3.root_analysis, type="test_type1", value="test_value_asdf", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=submission3.root_analysis, type="test_type2", value="test_value1", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=submission3.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # There should be 4 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 4

    # There should only be 1 submission when we filter by the test_value_asdf observable value
    get = client.get("/api/submission/?observable_value=test_value_asdf")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission3.uuid)

    # There should be 2 submissions when we filter by the test_value1 observable value
    get = client.get("/api/submission/?observable_value=test_value1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission3.uuid) for a in get.json()["items"])

    # There should be 3 submissions when we filter by the test_value1 and test_value2 observable values
    get = client.get("/api/submission/?observable_value=test_value1&observable_value=test_value2")
    assert get.json()["total"] == 3
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission3.uuid) for a in get.json()["items"])


def test_get_filter_observable_and_observable_types(client, db):
    # Create an empty submission
    factory.submission.create(db=db)

    # Create an submission with multiple observables
    submission2 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission2.root_analysis, type="test_type1", value="test_value1", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=submission2.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # Create an submission with one observable
    submission3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        parent_analysis=submission3.root_analysis, type="test_type1", value="test_value1", db=db
    )

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should only be 1 submission when we filter by observable and observable_types
    get = client.get("/api/submission/?observable_types=test_type1&observable=test_type2|test_value2")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)


def test_get_filter_owner(client, db):
    factory.submission.create(db=db)
    factory.submission.create(db=db, owner="analyst")

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by the owner
    get = client.get("/api/submission/?owner=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["owner"]["username"] == "analyst"

    # There should only be 1 submission when we filter by none
    get = client.get("/api/submission/?owner=none")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["owner"] is None

    # There should be 2 submissions when we filter by none and owner
    get = client.get("/api/submission/?owner=none&owner=analyst")
    assert get.json()["total"] == 2


def test_get_filter_queue(client, db):
    factory.submission.create(db=db, alert_queue="test_queue1")
    factory.submission.create(db=db, alert_queue="test_queue2")

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by the submission queue
    get = client.get("/api/submission/?queue=test_queue1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["queue"]["value"] == "test_queue1"

    # There should be 2 submission when we filter by multiple queues
    get = client.get("/api/submission/?queue=test_queue1&queue=test_queue2")
    assert get.json()["total"] == 2


def test_get_filter_submission_type(client, db):
    factory.submission.create(db=db, submission_type="test_type")
    factory.submission.create(db=db, submission_type="test_type2")

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by the submission type
    get = client.get("/api/submission/?submission_type=test_type")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type"

    # There should be 2 submissions when we filter by multiple submission types
    get = client.get("/api/submission/?submission_type=test_type&submission_type=test_type2")
    assert get.json()["total"] == 2


def test_get_filter_tags(client, db):
    submission1 = factory.submission.create(db=db, tags=["submission_tag"])
    factory.observable.create_or_read(
        type="fqdn", value="bad.com", parent_analysis=submission1.root_analysis, db=db, analysis_tags=["obs1"]
    )
    submission2 = factory.submission.create(db=db, tags=["tag2", "tag3", "tag4"])
    factory.submission.create(db=db, tags=["tag1"])

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should only be 1 submission when we filter by tag1
    get = client.get("/api/submission/?tags=tag1")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["tags"]) == 1
    assert get.json()["items"][0]["tags"][0]["value"] == "tag1"

    # There should only be 1 submission when we filter by tag2 AND tag3
    get = client.get("/api/submission/?tags=tag2,tag3")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["tags"]) == 3
    assert any(t["value"] == "tag2" for t in get.json()["items"][0]["tags"])
    assert any(t["value"] == "tag3" for t in get.json()["items"][0]["tags"])

    # There should only be 1 submission when we filter by the child observable tag obs1
    get = client.get("/api/submission/?tags=obs1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert len(get.json()["items"][0]["child_analysis_tags"]) == 1
    assert get.json()["items"][0]["child_analysis_tags"][0]["value"] == "obs1"

    # There should be 2 submissions when we filter by multiple tags
    get = client.get("/api/submission/?tags=tag2,tag3&tags=obs1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])


def test_get_filter_tool(client, db):
    submission1 = factory.submission.create(db=db, tool="test_tool1")
    submission2 = factory.submission.create(db=db, tool="test_tool2")

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by the tool
    get = client.get("/api/submission/?tool=test_tool1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["tool"]["value"] == "test_tool1"

    # There should be 2 submission when we filter by multiple tools
    get = client.get("/api/submission/?tool=test_tool1&tool=test_tool2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])


def test_get_filter_tool_instance(client, db):
    submission1 = factory.submission.create(db=db, tool_instance="test_tool_instance1")
    submission2 = factory.submission.create(db=db, tool_instance="test_tool_instance2")

    # There should be 2 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 2

    # There should only be 1 submission when we filter by the tool
    get = client.get("/api/submission/?tool_instance=test_tool_instance1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["tool_instance"]["value"] == "test_tool_instance1"

    # There should be 2 submission when we filter by multiple tools
    get = client.get("/api/submission/?tool_instance=test_tool_instance1&tool_instance=test_tool_instance2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(submission1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(submission2.uuid) for a in get.json()["items"])


def test_get_multiple_filters(client, db):
    factory.submission.create(db=db, submission_type="test_type1")
    factory.submission.create(db=db, submission_type="test_type1", disposition="FALSE_POSITIVE")
    factory.submission.create(db=db, submission_type="test_type2", disposition="FALSE_POSITIVE")

    # There should be 3 total submissions
    get = client.get("/api/submission/")
    assert get.json()["total"] == 3

    # There should only be 1 submission when we filter by the submission type and disposition
    get = client.get("/api/submission/?submission_type=test_type1&disposition=FALSE_POSITIVE")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type1"
    assert get.json()["items"][0]["disposition"]["value"] == "FALSE_POSITIVE"


def test_get_sort_by_submission_type(client, db):
    submission1 = factory.submission.create(db=db, submission_type="type1")
    submission2 = factory.submission.create(db=db, submission_type="type2")

    # If you sort descending, submission2 should appear first
    get = client.get("/api/submission/?sort=submission_type|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission1.uuid)

    # If you sort ascending, submission1 should appear first
    get = client.get("/api/submission/?sort=submission_type|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)


def test_get_sort_by_disposition(client, db):
    submission1 = factory.submission.create(db=db, disposition="DELIVERY")
    submission2 = factory.submission.create(db=db, disposition="FALSE_POSITIVE")
    submission3 = factory.submission.create(db=db)

    # If you sort descending: null disposition, FALSE_POSITIVE, DELIVERY
    get = client.get("/api/submission/?sort=disposition|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(submission3.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][2]["uuid"] == str(submission1.uuid)

    # If you sort ascending: DELIVERY, FALSE_POSITIVE, null disposition
    get = client.get("/api/submission/?sort=disposition|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][2]["uuid"] == str(submission3.uuid)


def test_get_sort_by_disposition_time(client, db):
    now = crud.helpers.utcnow()
    submission1 = factory.submission.create(db=db, disposition="FALSE_POSITIVE", update_time=now)
    submission2 = factory.submission.create(db=db, disposition="FALSE_POSITIVE", update_time=now + timedelta(seconds=5))

    # If you sort descending, the newest submission (submission2) should appear first
    get = client.get("/api/submission/?sort=disposition_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission1.uuid)

    # If you sort ascending, the oldest submission (submission1) should appear first
    get = client.get("/api/submission/?sort=disposition_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)


def test_get_sort_by_disposition_user(client, db):
    submission1 = factory.submission.create(db=db, disposition="FALSE_POSITIVE", updated_by_user="alice")
    submission2 = factory.submission.create(db=db, disposition="FALSE_POSITIVE", updated_by_user="bob")
    submission3 = factory.submission.create(db=db)

    # If you sort descending: null user, bob, alice
    get = client.get("/api/submission/?sort=disposition_user|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(submission3.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][2]["uuid"] == str(submission1.uuid)

    # If you sort ascending: alice, bob, null user
    get = client.get("/api/submission/?sort=disposition_user|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][2]["uuid"] == str(submission3.uuid)


def test_get_sort_by_event_time(client, db):
    now = crud.helpers.utcnow()
    submission1 = factory.submission.create(db=db, event_time=now)
    submission2 = factory.submission.create(db=db, event_time=now + timedelta(seconds=5))

    # If you sort descending, the newest submission (submission2) should appear first
    get = client.get("/api/submission/?sort=event_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission1.uuid)

    # If you sort ascending, the oldest submission (submission1) should appear first
    get = client.get("/api/submission/?sort=event_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)


def test_get_sort_by_insert_time(client, db):
    now = crud.helpers.utcnow()
    submission1 = factory.submission.create(db=db, insert_time=now)
    submission2 = factory.submission.create(db=db, insert_time=now + timedelta(seconds=5))

    # If you sort descending, the newest submission (submission2) should appear first
    get = client.get("/api/submission/?sort=insert_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission1.uuid)

    # If you sort ascending, the oldest submission (submission1) should appear first
    get = client.get("/api/submission/?sort=insert_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)


def test_get_sort_by_name(client, db):
    submission1 = factory.submission.create(db=db, name="submission1")
    submission2 = factory.submission.create(db=db, name="submission2")

    # If you sort descending, submission2 should appear first
    get = client.get("/api/submission/?sort=name|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission1.uuid)

    # If you sort ascending, submission1 should appear first
    get = client.get("/api/submission/?sort=name|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)


def test_get_sort_by_owner(client, db):
    submission1 = factory.submission.create(db=db, owner="alice")
    submission2 = factory.submission.create(db=db, owner="bob")
    submission3 = factory.submission.create(db=db)

    # If you sort descending: null owner, bob, alice
    get = client.get("/api/submission/?sort=owner|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(submission3.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][2]["uuid"] == str(submission1.uuid)

    # If you sort ascending: alice, bob, null owner
    get = client.get("/api/submission/?sort=owner|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][2]["uuid"] == str(submission3.uuid)


def test_get_sort_by_queue(client, db):
    submission1 = factory.submission.create(db=db, alert_queue="detect")
    submission2 = factory.submission.create(db=db, alert_queue="intel")

    # If you sort descending, submission2 should appear first
    get = client.get("/api/submission/?sort=queue|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission2.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission1.uuid)

    # If you sort ascending, submission1 should appear first
    get = client.get("/api/submission/?sort=queue|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(submission1.uuid)
    assert get.json()["items"][1]["uuid"] == str(submission2.uuid)


def test_get_submission_tree(client, db):
    submission = factory.submission.create_from_json_file(
        db=db, json_path="/app/tests/alerts/small.json", submission_name="Test Alert"
    )

    # The small.json submission has 14 observables and 16 analyses (the Root Analysis is not included in the tree).
    get = client.get(f"/api/submission/{submission.uuid}")
    assert str(get.json()["root_analysis"]["children"]).count("'observable'") == 14
    assert str(get.json()["root_analysis"]["children"]).count("'analysis'") == 16
    assert len(get.json()["root_analysis"]["children"]) == 2


def test_get_submissions_observables(client, db):
    # Create an submission tree where the same observable type+value appears twice
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
    get = client.post("/api/submission/observables", json=[str(submission.uuid), str(submission2.uuid)])
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 3
    assert any(o["type"]["value"] == "email_address" and o["value"] == "badguy@bad.com" for o in get.json())
    assert any(o["type"]["value"] == "fqdn" and o["value"] == "bad.com" for o in get.json())
    assert any(o["type"]["value"] == "ipv4" and o["value"] == "127.0.0.1" for o in get.json())


def test_read_summary_url_domain(client, db):
    # Create a submission
    submission1 = factory.submission.create(db=db)

    # The URL domains summary should be empty
    get = client.get(f"/api/submission/{submission1.uuid}/summary/url_domain")
    assert get.json() == {"domains": [], "total": 0}

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
    get = client.get(f"/api/submission/{submission1.uuid}/summary/url_domain")
    assert get.json()["total"] == 4
    assert len(get.json()["domains"]) == 3
    assert get.json()["domains"][0]["domain"] == "example.com"
    assert get.json()["domains"][0]["count"] == 2
    assert get.json()["domains"][1]["domain"] == "example2.com"
    assert get.json()["domains"][1]["count"] == 1
    assert get.json()["domains"][2]["domain"] == "example3.com"
    assert get.json()["domains"][2]["count"] == 1
