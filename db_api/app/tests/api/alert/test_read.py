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
    get = client.get("/api/alert/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/alert/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all_pagination(client, db):
    # Create 11 alerts
    for _ in range(11):
        factory.alert.create(db=db)

    # Keep track of all of the alert UUIDs to make sure we read them all
    unique_alert_uuids = set()

    # Read every page in chunks of 2 while there are still results
    offset = 0
    while True:
        get = client.get(f"/api/alert/?limit=2&offset={offset}")

        # Store the alert UUIDs
        for alert in get.json()["items"]:
            unique_alert_uuids.add(alert["uuid"])

            # Make sure the node_type field is "alert"
            assert alert["node_type"] == "alert"

        # Check if there is another page to retrieve
        if len(unique_alert_uuids) < get.json()["total"]:
            # Increase the offset to get the next page
            offset += get.json()["limit"]
            continue

        break

    # Should have gotten all 11 alerts across the pages
    assert len(unique_alert_uuids) == 11


def test_get_all_empty(client):
    get = client.get("/api/alert/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {"items": [], "limit": 50, "offset": 0, "total": 0}


def test_get_filter_disposition(client, db):
    factory.alert.create(db=db)
    factory.alert.create(db=db, disposition="FALSE_POSITIVE")

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the disposition
    get = client.get("/api/alert/?disposition=none")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["disposition"] is None


def test_get_filter_disposition_user(client, db):
    factory.alert.create(db=db, history_username="analyst")
    alert = factory.alert.create(
        db=db, disposition="FALSE_POSITIVE", updated_by_user="analyst", history_username="analyst"
    )

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the disposition user
    get = client.get("/api/alert/?disposition_user=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert.uuid)


def test_get_filter_disposition_user_multiple(client, db):
    factory.alert.create(db=db, history_username="analyst")

    # This alert was first dispositioned by alice
    alert = factory.alert.create(db=db, disposition="FALSE_POSITIVE", updated_by_user="alice", history_username="alice")

    # This alert was first dispositioned by analyst
    factory.alert.create(db=db, disposition="FALSE_POSITIVE", updated_by_user="analyst", history_username="analyst")

    # analyst re-dispositions alice's alert
    update = client.patch(
        "/api/alert/?history_username=analyst", json=[{"disposition": "DELIVERY", "uuid": str(alert.uuid)}]
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the alert is no longer dispositioned by alice
    get = client.get(f"/api/alert/{alert.uuid}")
    assert get.json()["disposition_user"]["username"] == "analyst"

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should still be 1 alert when we filter by the disposition user alice
    get = client.get("/api/alert/?disposition_user=alice")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert.uuid)


def test_get_filter_dispositioned_after(client, db):
    now = crud.helpers.utcnow()
    factory.alert.create(db=db, history_username="analyst")
    factory.alert.create(db=db, disposition="FALSE_POSITIVE", update_time=now, history_username="analyst")
    factory.alert.create(
        db=db, disposition="FALSE_POSITIVE", update_time=now + timedelta(seconds=5), history_username="analyst"
    )

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by dispositioned_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"dispositioned_after": now}
    get = client.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_dispositioned_before(client, db):
    now = crud.helpers.utcnow()
    factory.alert.create(db=db, history_username="analyst")
    factory.alert.create(
        db=db, disposition="FALSE_POSITIVE", update_time=now - timedelta(seconds=5), history_username="analyst"
    )
    factory.alert.create(db=db, disposition="FALSE_POSITIVE", update_time=now, history_username="analyst")

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by dispositioned_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"dispositioned_before": now}
    get = client.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_dispositioned_after_and_before(client, db):
    now = crud.helpers.utcnow()
    after = now - timedelta(days=1)
    before = now + timedelta(days=1)
    factory.alert.create(db=db, disposition="FALSE_POSITIVE", update_time=after, history_username="analyst")
    factory.alert.create(db=db, disposition="FALSE_POSITIVE", update_time=now, history_username="analyst")
    factory.alert.create(db=db, disposition="FALSE_POSITIVE", update_time=before, history_username="analyst")

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by dispositioned_after and dispositioned_before.
    # But the timestamp has a timezone specified, which uses the + symbol that needs to be
    # urlencoded since it is a reserved URL character.
    params = {
        "dispositioned_after": after,
        "dispositioned_before": before,
    }
    get = client.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_after(client, db):
    now = crud.helpers.utcnow()
    alert = factory.alert.create(db=db, event_time=now)
    factory.alert.create(db=db, event_time=now + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by event_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"event_time_after": alert.event_time}
    get = client.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_before(client, db):
    now = crud.helpers.utcnow()
    factory.alert.create(db=db, event_time=now)
    alert = factory.alert.create(db=db, event_time=now + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by event_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"event_time_before": alert.event_time}
    get = client.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_uuid(client, db):
    # Create an event
    event = helpers.create_event(name="Test Event", db=db)

    # Create some alerts
    factory.alert.create(db=db)
    alert = factory.alert.create(db=db, event=event)

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the event_uuid
    get = client.get(f"/api/alert/?event_uuid={event.uuid}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert.uuid)
    assert get.json()["items"][0]["event_uuid"] == str(event.uuid)


def test_get_filter_insert_time_after(client, db):
    now = crud.helpers.utcnow()
    alert = factory.alert.create(db=db, insert_time=now)
    factory.alert.create(db=db, insert_time=now + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by insert_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"insert_time_after": alert.insert_time}
    get = client.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_insert_time_before(client, db):
    now = crud.helpers.utcnow()
    factory.alert.create(db=db, insert_time=now - timedelta(seconds=5))
    alert = factory.alert.create(db=db, insert_time=now)

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by insert_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"insert_time_before": alert.insert_time}
    get = client.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_name(client, db):
    factory.alert.create(db=db, name="Test Alert")
    factory.alert.create(db=db, name="Some Other Alert")

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the name
    get = client.get("/api/alert/?name=test alert")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "Test Alert"


def test_get_filter_observable(client, db):
    # Create an empty alert
    factory.alert.create(db=db)

    # Create some alerts with one observable
    alert1 = factory.alert.create(db=db)
    alert1.root_observables = [factory.observable.create(type="test_type1", value="test_value1", db=db)]

    alert2 = factory.alert.create(db=db)
    alert2.root_observables = [factory.observable.create(type="test_type2", value="test_value2", db=db)]

    # Create an alert with multiple observables
    alert3 = factory.alert.create(db=db)
    alert3.root_observables = [
        factory.observable.create(type="test_type1", value="test_value_asdf", db=db),
        factory.observable.create(type="test_type2", value="test_value1", db=db),
        factory.observable.create(type="test_type2", value="test_value2", db=db),
    ]

    # There should be 4 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 4

    # There should only be 1 alert when we filter by the test_type1/test_value1 observable
    get = client.get("/api/alert/?observable=test_type1|test_value1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)

    # There should be 2 alerts when we filter by the test_type2/test_value2 observable
    get = client.get("/api/alert/?observable=test_type2|test_value2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(alert2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(alert3.uuid) for a in get.json()["items"])


def test_get_filter_observable_types(client, db):
    # Create an empty alert
    factory.alert.create(db=db)

    # Create an alert with one observable
    alert1 = factory.alert.create(db=db)
    factory.observable.create(parent_tree=alert1, type="test_type1", value="test_value1", db=db)

    # Create an alert with multiple observables
    alert2 = factory.alert.create(db=db)
    factory.observable.create(parent_tree=alert2, type="test_type1", value="test_value_asdf", db=db)
    factory.observable.create(parent_tree=alert2, type="test_type2", value="test_value1", db=db)
    factory.observable.create(parent_tree=alert2, type="test_type2", value="test_value2", db=db)

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should be 2 alerts when we filter by just test_type1
    get = client.get("/api/alert/?observable_types=test_type1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(alert1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(alert2.uuid) for a in get.json()["items"])

    # There should only be 1 alert when we filter by the test_type1 and test_type2
    get = client.get("/api/alert/?observable_types=test_type1,test_type2")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert2.uuid)


def test_get_filter_observable_value(client, db):
    # Create an empty alert
    factory.alert.create(db=db)

    # Create some alerts with one observable
    alert1 = factory.alert.create(db=db)
    factory.observable.create(parent_tree=alert1, type="test_type1", value="test_value1", db=db)

    alert2 = factory.alert.create(db=db)
    factory.observable.create(parent_tree=alert2, type="test_type2", value="test_value2", db=db)

    # Create an alert with multiple observables
    alert3 = factory.alert.create(db=db)
    factory.observable.create(parent_tree=alert3, type="test_type1", value="test_value_asdf", db=db)
    factory.observable.create(parent_tree=alert3, type="test_type2", value="test_value1", db=db)
    factory.observable.create(parent_tree=alert3, type="test_type2", value="test_value2", db=db)

    # There should be 4 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 4

    # There should only be 1 alert when we filter by the test_value_asdf observable value
    get = client.get("/api/alert/?observable_value=test_value_asdf")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert3.uuid)

    # There should be 2 alerts when we filter by the test_value1 observable value
    get = client.get("/api/alert/?observable_value=test_value1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(alert1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(alert3.uuid) for a in get.json()["items"])


def test_get_filter_observable_and_observable_types(client, db):
    # Create an empty alert
    factory.alert.create(db=db)

    # Create an alert with multiple observables
    alert2 = factory.alert.create(db=db)
    factory.observable.create(parent_tree=alert2, type="test_type1", value="test_value1", db=db)
    factory.observable.create(parent_tree=alert2, type="test_type2", value="test_value2", db=db)

    # Create an alert with one observable
    alert3 = factory.alert.create(db=db)
    factory.observable.create(parent_tree=alert3, type="test_type1", value="test_value1", db=db)

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by observable and observable_types
    get = client.get("/api/alert/?observable_types=test_type1&observable=test_type2|test_value2")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert2.uuid)


def test_get_filter_owner(client, db):
    factory.alert.create(db=db)
    factory.alert.create(db=db, owner="analyst")

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the owner
    get = client.get("/api/alert/?owner=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["owner"]["username"] == "analyst"


def test_get_filter_queue(client, db):
    factory.alert.create(db=db, alert_queue="test_queue1")
    factory.alert.create(db=db, alert_queue="test_queue2")

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the alert queue
    get = client.get("/api/alert/?queue=test_queue1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["queue"]["value"] == "test_queue1"


def test_get_filter_tags(client, db):
    alert1 = factory.alert.create(db=db, tags=["alert_tag"])
    factory.observable.create(type="fqdn", value="bad.com", parent_tree=alert1, db=db, tags=["obs1"])
    factory.alert.create(db=db, tags=["tag1"])
    factory.alert.create(db=db, tags=["tag2", "tag3", "tag4"])

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by tag1
    get = client.get("/api/alert/?tags=tag1")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["tags"]) == 1
    assert get.json()["items"][0]["tags"][0]["value"] == "tag1"

    # There should only be 1 alert when we filter by tag2 AND tag3
    get = client.get("/api/alert/?tags=tag2,tag3")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["tags"]) == 3
    assert any(t["value"] == "tag2" for t in get.json()["items"][0]["tags"])
    assert any(t["value"] == "tag3" for t in get.json()["items"][0]["tags"])

    # There should only be 1 alert when we filter by the child observable tag obs1
    get = client.get("/api/alert/?tags=obs1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert len(get.json()["items"][0]["child_tags"]) == 1
    assert get.json()["items"][0]["child_tags"][0]["value"] == "obs1"

    # All the alerts should be returned if you don't specify any tags for the filter
    get = client.get("/api/alert/?tags=")
    assert get.json()["total"] == 3


def test_get_filter_threat_actors(client, db):
    alert1 = factory.alert.create(db=db)
    factory.observable.create(
        type="fqdn", value="bad.com", parent_analysis=alert1.root_analysis, db=db, threat_actors=["bad_guys"]
    )
    factory.alert.create(db=db, threat_actors=["test_actor"])

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should be 1 alert when we filter test_actor
    get = client.get("/api/alert/?threat_actors=test_actor")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["threat_actors"][0]["value"] == "test_actor"

    # There should be 1 alert when we filter by the child observable threat_actor
    get = client.get("/api/alert/?threat_actors=bad_guys")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["child_threat_actors"]) == 1
    assert get.json()["items"][0]["child_threat_actors"][0]["value"] == "bad_guys"

    # All the alerts should be returned if you don't specify anything for the filter
    get = client.get("/api/alert/?threat_actors=")
    assert get.json()["total"] == 2


def test_get_filter_threats(client, db):
    alert1 = factory.alert.create(db=db)
    factory.observable.create(
        type="fqdn", value="bad.com", parent_analysis=alert1.root_analysis, db=db, threats=["malz"]
    )
    factory.alert.create(db=db, threats=["threat1"])
    factory.alert.create(db=db, threats=["threat2", "threat3", "threat4"])

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should be 1 alert when we filter by threat1
    get = client.get("/api/alert/?threats=threat1")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["threats"]) == 1
    assert get.json()["items"][0]["threats"][0]["value"] == "threat1"

    # There should be 1 alert when we filter by threat2 AND threat3
    get = client.get("/api/alert/?threats=threat2,threat3")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["threats"]) == 3
    assert any(t["value"] == "threat2" for t in get.json()["items"][0]["threats"])
    assert any(t["value"] == "threat3" for t in get.json()["items"][0]["threats"])

    # There should be 1 alert when we filter by the child observable threat
    get = client.get("/api/alert/?threats=malz")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["child_threats"]) == 1
    assert get.json()["items"][0]["child_threats"][0]["value"] == "malz"

    # All the alerts should be returned if you don't specify any threats for the filter
    get = client.get("/api/alert/?threats=")
    assert get.json()["total"] == 3


def test_get_filter_tool(client, db):
    factory.alert.create(db=db, tool="test_tool1")
    factory.alert.create(db=db, tool="test_tool2")

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the tool
    get = client.get("/api/alert/?tool=test_tool1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["tool"]["value"] == "test_tool1"


def test_get_filter_tool_instance(client, db):
    factory.alert.create(db=db, tool_instance="test_tool_instance1")
    factory.alert.create(db=db, tool_instance="test_tool_instance2")

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the tool
    get = client.get("/api/alert/?tool_instance=test_tool_instance1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["tool_instance"]["value"] == "test_tool_instance1"


def test_get_filter_type(client, db):
    factory.alert.create(db=db, alert_type="test_type")
    factory.alert.create(db=db, alert_type="test_type2")

    # There should be 2 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the alert type
    get = client.get("/api/alert/?type=test_type")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type"


def test_get_multiple_filters(client, db):
    factory.alert.create(db=db, alert_type="test_type1")
    factory.alert.create(db=db, alert_type="test_type1", disposition="FALSE_POSITIVE")
    factory.alert.create(db=db, alert_type="test_type2", disposition="FALSE_POSITIVE")

    # There should be 3 total alerts
    get = client.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by the alert type and disposition
    get = client.get("/api/alert/?type=test_type1&disposition=FALSE_POSITIVE")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type1"
    assert get.json()["items"][0]["disposition"]["value"] == "FALSE_POSITIVE"


def test_get_sort_by_disposition(client, db):
    alert1 = factory.alert.create(db=db, disposition="DELIVERY")
    alert2 = factory.alert.create(db=db, disposition="FALSE_POSITIVE")
    alert3 = factory.alert.create(db=db)

    # If you sort descending: null disposition, FALSE_POSITIVE, DELIVERY
    get = client.get("/api/alert/?sort=disposition|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert3.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][2]["uuid"] == str(alert1.uuid)

    # If you sort ascending: DELIVERY, FALSE_POSITIVE, null disposition
    get = client.get("/api/alert/?sort=disposition|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][2]["uuid"] == str(alert3.uuid)


def test_get_sort_by_disposition_time(client, db):
    now = crud.helpers.utcnow()
    alert1 = factory.alert.create(db=db, disposition="FALSE_POSITIVE", update_time=now)
    alert2 = factory.alert.create(db=db, disposition="FALSE_POSITIVE", update_time=now + timedelta(seconds=5))

    # If you sort descending, the newest alert (alert2) should appear first
    get = client.get("/api/alert/?sort=disposition_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert1.uuid)

    # If you sort ascending, the oldest alert (alert1) should appear first
    get = client.get("/api/alert/?sort=disposition_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)


def test_get_sort_by_disposition_user(client, db):
    alert1 = factory.alert.create(db=db, disposition="FALSE_POSITIVE", updated_by_user="alice")
    alert2 = factory.alert.create(db=db, disposition="FALSE_POSITIVE", updated_by_user="bob")
    alert3 = factory.alert.create(db=db)

    # If you sort descending: null user, bob, alice
    get = client.get("/api/alert/?sort=disposition_user|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert3.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][2]["uuid"] == str(alert1.uuid)

    # If you sort ascending: alice, bob, null user
    get = client.get("/api/alert/?sort=disposition_user|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][2]["uuid"] == str(alert3.uuid)


def test_get_sort_by_event_time(client, db):
    now = crud.helpers.utcnow()
    alert1 = factory.alert.create(db=db, event_time=now)
    alert2 = factory.alert.create(db=db, event_time=now + timedelta(seconds=5))

    # If you sort descending, the newest alert (alert2) should appear first
    get = client.get("/api/alert/?sort=event_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert1.uuid)

    # If you sort ascending, the oldest alert (alert1) should appear first
    get = client.get("/api/alert/?sort=event_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)


def test_get_sort_by_insert_time(client, db):
    now = crud.helpers.utcnow()
    alert1 = factory.alert.create(db=db, insert_time=now)
    alert2 = factory.alert.create(db=db, insert_time=now + timedelta(seconds=5))

    # If you sort descending, the newest alert (alert2) should appear first
    get = client.get("/api/alert/?sort=insert_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert1.uuid)

    # If you sort ascending, the oldest alert (alert1) should appear first
    get = client.get("/api/alert/?sort=insert_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)


def test_get_sort_by_name(client, db):
    alert1 = factory.alert.create(db=db, name="alert1")
    alert2 = factory.alert.create(db=db, name="alert2")

    # If you sort descending, alert2 should appear first
    get = client.get("/api/alert/?sort=name|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert1.uuid)

    # If you sort ascending, alert1 should appear first
    get = client.get("/api/alert/?sort=name|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)


def test_get_sort_by_owner(client, db):
    alert1 = factory.alert.create(db=db, owner="alice")
    alert2 = factory.alert.create(db=db, owner="bob")
    alert3 = factory.alert.create(db=db)

    # If you sort descending: null owner, bob, alice
    get = client.get("/api/alert/?sort=owner|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert3.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][2]["uuid"] == str(alert1.uuid)

    # If you sort ascending: alice, bob, null owner
    get = client.get("/api/alert/?sort=owner|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][2]["uuid"] == str(alert3.uuid)


def test_get_sort_by_queue(client, db):
    alert1 = factory.alert.create(db=db, alert_queue="detect")
    alert2 = factory.alert.create(db=db, alert_queue="intel")

    # If you sort descending, alert2 should appear first
    get = client.get("/api/alert/?sort=queue|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert1.uuid)

    # If you sort ascending, alert1 should appear first
    get = client.get("/api/alert/?sort=queue|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)


def test_get_sort_by_type(client, db):
    alert1 = factory.alert.create(db=db, alert_type="type1")
    alert2 = factory.alert.create(db=db, alert_type="type2")

    # If you sort descending, alert2 should appear first
    get = client.get("/api/alert/?sort=type|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert2.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert1.uuid)

    # If you sort ascending, alert1 should appear first
    get = client.get("/api/alert/?sort=type|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert1.uuid)
    assert get.json()["items"][1]["uuid"] == str(alert2.uuid)


def test_get_alert_tree(client, db):
    alert = factory.alert.create_from_json_file(
        db=db, json_path="/app/tests/alerts/small.json", alert_name="Test Alert"
    )

    # The small.json alert has 14 observables and 16 analyses (the Root Analysis is not included in the tree).
    get = client.get(f"/api/alert/{alert.uuid}")
    assert str(get.json()["children"]).count("'observable'") == 14
    assert str(get.json()["children"]).count("'analysis'") == 16
    assert len(get.json()["children"]) == 2
