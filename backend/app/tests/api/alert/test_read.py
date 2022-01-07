import uuid

from datetime import datetime, timedelta
from fastapi import status
from urllib.parse import urlencode

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client_valid_access_token):
    get = client_valid_access_token.get("/api/alert/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client_valid_access_token):
    get = client_valid_access_token.get(f"/api/alert/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all_pagination(client_valid_access_token, db):
    # Create 11 alerts
    for _ in range(11):
        helpers.create_alert(db)

    # Keep track of all of the alert UUIDs to make sure we read them all
    unique_alert_uuids = set()

    # Read every page in chunks of 2 while there are still results
    offset = 0
    while True:
        get = client_valid_access_token.get(f"/api/alert/?limit=2&offset={offset}")

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


def test_get_all_empty(client_valid_access_token):
    get = client_valid_access_token.get("/api/alert/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {"items": [], "limit": 50, "offset": 0, "total": 0}


def test_get_filter_disposition(client_valid_access_token, db):
    helpers.create_alert(db)
    helpers.create_alert(db, disposition="FALSE_POSITIVE")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the disposition
    get = client_valid_access_token.get("/api/alert/?disposition=none")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["disposition"] is None


def test_get_filter_disposition_user(client_valid_access_token, db):
    helpers.create_alert(db)
    helpers.create_alert(db, disposition_user="analyst")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the disposition user
    get = client_valid_access_token.get("/api/alert/?disposition_user=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["disposition_user"]["username"] == "analyst"


def test_get_filter_dispositioned_after(client_valid_access_token, db):
    helpers.create_alert(db)
    alert_tree2 = helpers.create_alert(db, disposition_time=datetime.utcnow())
    helpers.create_alert(db, disposition_time=datetime.utcnow() + timedelta(seconds=5))

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by dispositioned_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"dispositioned_after": alert_tree2.node.disposition_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_dispositioned_before(client_valid_access_token, db):
    helpers.create_alert(db)
    helpers.create_alert(db, disposition_time=datetime.utcnow() - timedelta(seconds=5))
    alert_tree3 = helpers.create_alert(db, disposition_time=datetime.utcnow())

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by dispositioned_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"dispositioned_before": alert_tree3.node.disposition_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_dispositioned_after_and_before(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, disposition_time=datetime.utcnow() - timedelta(days=1))
    helpers.create_alert(db, disposition_time=datetime.utcnow())
    alert_tree3 = helpers.create_alert(db, disposition_time=datetime.utcnow() + timedelta(days=1))

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by dispositioned_after and dispositioned_before.
    # But the timestamp has a timezone specified, which uses the + symbol that needs to be
    # urlencoded since it is a reserved URL character.
    params = {
        "dispositioned_after": alert_tree1.node.disposition_time,
        "dispositioned_before": alert_tree3.node.disposition_time,
    }
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_after(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, event_time=datetime.utcnow())
    helpers.create_alert(db, event_time=datetime.utcnow() + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by event_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"event_time_after": alert_tree1.node.event_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_before(client_valid_access_token, db):
    helpers.create_alert(db, event_time=datetime.utcnow())
    alert_tree2 = helpers.create_alert(db, event_time=datetime.utcnow() + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by event_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"event_time_before": alert_tree2.node.event_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_uuid(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="Test Event", db=db)

    # Create some alerts
    helpers.create_alert(db)
    alert_tree2 = helpers.create_alert(db)

    # Add one alert to the event
    alert_tree2.node.event_uuid = event.uuid

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the event_uuid
    get = client_valid_access_token.get(f"/api/alert/?event_uuid={event.uuid}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["event_uuid"] == str(event.uuid)


def test_get_filter_insert_time_after(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, insert_time=datetime.utcnow())
    helpers.create_alert(db, insert_time=datetime.utcnow() + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by insert_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"insert_time_after": alert_tree1.node.insert_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_insert_time_before(client_valid_access_token, db):
    helpers.create_alert(db, insert_time=datetime.utcnow() - timedelta(seconds=5))
    alert_tree2 = helpers.create_alert(db, insert_time=datetime.utcnow())

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by insert_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"insert_time_before": alert_tree2.node.insert_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_name(client_valid_access_token, db):
    helpers.create_alert(db, name="Test Alert")
    helpers.create_alert(db, name="Some Other Alert")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the name
    get = client_valid_access_token.get("/api/alert/?name=test alert")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "Test Alert"


def test_get_filter_observable(client_valid_access_token, db):
    # Create an empty alert
    helpers.create_alert(db=db)

    # Create some alerts with one observable
    alert_tree1 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree1, type="test_type1", value="test_value1", db=db)

    alert_tree2 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree2, type="test_type2", value="test_value2", db=db)

    # Create an alert with multiple observables
    alert_tree3 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree3, type="test_type1", value="test_value_asdf", db=db)
    helpers.create_observable(parent_tree=alert_tree3, type="test_type2", value="test_value1", db=db)
    helpers.create_observable(parent_tree=alert_tree3, type="test_type2", value="test_value2", db=db)

    # There should be 4 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 4

    # There should only be 1 alert when we filter by the test_type1/test_value1 observable
    get = client_valid_access_token.get("/api/alert/?observable=test_type1|test_value1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)

    # There should be 2 alerts when we filter by the test_type2/test_value2 observable
    get = client_valid_access_token.get("/api/alert/?observable=test_type2|test_value2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(alert_tree2.node_uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(alert_tree3.node_uuid) for a in get.json()["items"])


def test_get_filter_observable_types(client_valid_access_token, db):
    # Create an empty alert
    helpers.create_alert(db=db)

    # Create an alert with one observable
    alert_tree1 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree1, type="test_type1", value="test_value1", db=db)

    # Create an alert with multiple observables
    alert_tree2 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree2, type="test_type1", value="test_value_asdf", db=db)
    helpers.create_observable(parent_tree=alert_tree2, type="test_type2", value="test_value1", db=db)
    helpers.create_observable(parent_tree=alert_tree2, type="test_type2", value="test_value2", db=db)

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should be 2 alerts when we filter by just test_type1
    get = client_valid_access_token.get("/api/alert/?observable_types=test_type1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(alert_tree1.node_uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(alert_tree2.node_uuid) for a in get.json()["items"])

    # There should only be 1 alert when we filter by the test_type1 and test_type2
    get = client_valid_access_token.get("/api/alert/?observable_types=test_type1,test_type2")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert_tree2.node_uuid)


def test_get_filter_observable_value(client_valid_access_token, db):
    # Create an empty alert
    helpers.create_alert(db=db)

    # Create some alerts with one observable
    alert_tree1 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree1, type="test_type1", value="test_value1", db=db)

    alert_tree2 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree2, type="test_type2", value="test_value2", db=db)

    # Create an alert with multiple observables
    alert_tree3 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree3, type="test_type1", value="test_value_asdf", db=db)
    helpers.create_observable(parent_tree=alert_tree3, type="test_type2", value="test_value1", db=db)
    helpers.create_observable(parent_tree=alert_tree3, type="test_type2", value="test_value2", db=db)

    # There should be 4 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 4

    # There should only be 1 alert when we filter by the test_value_asdf observable value
    get = client_valid_access_token.get("/api/alert/?observable_value=test_value_asdf")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert_tree3.node_uuid)

    # There should be 2 alerts when we filter by the test_value1 observable value
    get = client_valid_access_token.get("/api/alert/?observable_value=test_value1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(alert_tree1.node_uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(alert_tree3.node_uuid) for a in get.json()["items"])


def test_get_filter_observable_and_observable_types(client_valid_access_token, db):
    # Create an empty alert
    helpers.create_alert(db=db)

    # Create an alert with multiple observables
    alert_tree2 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree2, type="test_type1", value="test_value1", db=db)
    helpers.create_observable(parent_tree=alert_tree2, type="test_type2", value="test_value2", db=db)

    # Create an alert with one observable
    alert_tree3 = helpers.create_alert(db=db)
    helpers.create_observable(parent_tree=alert_tree3, type="test_type1", value="test_value1", db=db)

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by observable and observable_types
    get = client_valid_access_token.get("/api/alert/?observable_types=test_type1&observable=test_type2|test_value2")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["uuid"] == str(alert_tree2.node_uuid)


def test_get_filter_owner(client_valid_access_token, db):
    helpers.create_user(username="analyst", db=db)
    helpers.create_alert(db)
    helpers.create_alert(db, owner="analyst")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the owner
    get = client_valid_access_token.get("/api/alert/?owner=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["owner"]["username"] == "analyst"


def test_get_filter_queue(client_valid_access_token, db):
    helpers.create_alert(db, alert_queue="test_queue1")
    helpers.create_alert(db, alert_queue="test_queue2")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the alert queue
    get = client_valid_access_token.get("/api/alert/?queue=test_queue1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["queue"]["value"] == "test_queue1"


def test_get_filter_tags(client_valid_access_token, db):
    helpers.create_alert(db)
    helpers.create_alert(db, tags=["tag1"])
    helpers.create_alert(db, tags=["tag2", "tag3", "tag4"])

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by a single tag
    get = client_valid_access_token.get("/api/alert/?tags=tag1")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["tags"]) == 1
    assert get.json()["items"][0]["tags"][0]["value"] == "tag1"

    # There should only be 1 alert when we filter by multiple tags
    get = client_valid_access_token.get("/api/alert/?tags=tag2,tag3")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["tags"]) == 3
    assert any(t["value"] == "tag2" for t in get.json()["items"][0]["tags"])
    assert any(t["value"] == "tag3" for t in get.json()["items"][0]["tags"])

    # All the alerts should be returned if you don't specify any tags for the filter
    get = client_valid_access_token.get("/api/alert/?tags=")
    assert get.json()["total"] == 3


def test_get_filter_threat_actors(client_valid_access_token, db):
    helpers.create_alert(db)
    helpers.create_alert(db, threat_actors=["test_actor"])

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by a single threat
    get = client_valid_access_token.get("/api/alert/?threat_actors=test_actor")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["threat_actors"][0]["value"] == "test_actor"

    # All the alerts should be returned if you don't specify anything for the filter
    get = client_valid_access_token.get("/api/alert/?threat_actors=")
    assert get.json()["total"] == 2


def test_get_filter_threats(client_valid_access_token, db):
    helpers.create_alert(db)
    helpers.create_alert(db, threats=["threat1"])
    helpers.create_alert(db, threats=["threat2", "threat3", "threat4"])

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by a single threat
    get = client_valid_access_token.get("/api/alert/?threats=threat1")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["threats"]) == 1
    assert get.json()["items"][0]["threats"][0]["value"] == "threat1"

    # There should only be 1 alert when we filter by multiple threats
    get = client_valid_access_token.get("/api/alert/?threats=threat2,threat3")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["threats"]) == 3
    assert any(t["value"] == "threat2" for t in get.json()["items"][0]["threats"])
    assert any(t["value"] == "threat3" for t in get.json()["items"][0]["threats"])

    # All the alerts should be returned if you don't specify any threats for the filter
    get = client_valid_access_token.get("/api/alert/?threats=")
    assert get.json()["total"] == 3


def test_get_filter_tool(client_valid_access_token, db):
    helpers.create_alert(db, tool="test_tool1")
    helpers.create_alert(db, tool="test_tool2")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the tool
    get = client_valid_access_token.get("/api/alert/?tool=test_tool1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["tool"]["value"] == "test_tool1"


def test_get_filter_tool_instance(client_valid_access_token, db):
    helpers.create_alert(db, tool_instance="test_tool_instance1")
    helpers.create_alert(db, tool_instance="test_tool_instance2")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the tool
    get = client_valid_access_token.get("/api/alert/?tool_instance=test_tool_instance1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["tool_instance"]["value"] == "test_tool_instance1"


def test_get_filter_type(client_valid_access_token, db):
    helpers.create_alert(db, alert_type="test_type")
    helpers.create_alert(db, alert_type="test_type2")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the alert type
    get = client_valid_access_token.get("/api/alert/?type=test_type")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type"


def test_get_multiple_filters(client_valid_access_token, db):
    helpers.create_alert(db, alert_type="test_type1")
    helpers.create_alert(db, alert_type="test_type1", disposition="FALSE_POSITIVE")
    helpers.create_alert(db, alert_type="test_type2", disposition="FALSE_POSITIVE")

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by the alert type and disposition
    get = client_valid_access_token.get("/api/alert/?type=test_type1&disposition=FALSE_POSITIVE")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type1"
    assert get.json()["items"][0]["disposition"]["value"] == "FALSE_POSITIVE"


def test_get_sort_by_disposition(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, disposition="DELIVERY")
    alert_tree2 = helpers.create_alert(db, disposition="FALSE_POSITIVE")
    alert_tree3 = helpers.create_alert(db)

    # If you sort descending: null disposition, FALSE_POSITIVE, DELIVERY
    get = client_valid_access_token.get("/api/alert/?sort=disposition|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert_tree3.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][2]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending: DELIVERY, FALSE_POSITIVE, null disposition
    get = client_valid_access_token.get("/api/alert/?sort=disposition|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][2]["uuid"] == str(alert_tree3.node_uuid)


def test_get_sort_by_disposition_time(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, disposition_time=datetime.utcnow())
    alert_tree2 = helpers.create_alert(db, disposition_time=datetime.utcnow() + timedelta(seconds=5))

    # If you sort descending, the newest alert (alert2) should appear first
    get = client_valid_access_token.get("/api/alert/?sort=disposition_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending, the oldest alert (alert1) should appear first
    get = client_valid_access_token.get("/api/alert/?sort=disposition_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)


def test_get_sort_by_disposition_user(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, disposition_user="alice")
    alert_tree2 = helpers.create_alert(db, disposition_user="bob")
    alert_tree3 = helpers.create_alert(db)

    # If you sort descending: null user, bob, alice
    get = client_valid_access_token.get("/api/alert/?sort=disposition_user|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert_tree3.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][2]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending: alice, bob, null user
    get = client_valid_access_token.get("/api/alert/?sort=disposition_user|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][2]["uuid"] == str(alert_tree3.node_uuid)


def test_get_sort_by_event_time(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, event_time=datetime.utcnow())
    alert_tree2 = helpers.create_alert(db, event_time=datetime.utcnow() + timedelta(seconds=5))

    # If you sort descending, the newest alert (alert2) should appear first
    get = client_valid_access_token.get("/api/alert/?sort=event_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending, the oldest alert (alert1) should appear first
    get = client_valid_access_token.get("/api/alert/?sort=event_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)


def test_get_sort_by_insert_time(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, insert_time=datetime.utcnow())
    alert_tree2 = helpers.create_alert(db, insert_time=datetime.utcnow() + timedelta(seconds=5))

    # If you sort descending, the newest alert (alert2) should appear first
    get = client_valid_access_token.get("/api/alert/?sort=insert_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending, the oldest alert (alert1) should appear first
    get = client_valid_access_token.get("/api/alert/?sort=insert_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)


def test_get_sort_by_name(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, name="alert1")
    alert_tree2 = helpers.create_alert(db, name="alert2")

    # If you sort descending, alert2 should appear first
    get = client_valid_access_token.get("/api/alert/?sort=name|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending, alert1 should appear first
    get = client_valid_access_token.get("/api/alert/?sort=name|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)


def test_get_sort_by_owner(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, owner="alice")
    alert_tree2 = helpers.create_alert(db, owner="bob")
    alert_tree3 = helpers.create_alert(db)

    # If you sort descending: null owner, bob, alice
    get = client_valid_access_token.get("/api/alert/?sort=owner|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert_tree3.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][2]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending: alice, bob, null owner
    get = client_valid_access_token.get("/api/alert/?sort=owner|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][2]["uuid"] == str(alert_tree3.node_uuid)


def test_get_sort_by_queue(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, alert_queue="detect")
    alert_tree2 = helpers.create_alert(db, alert_queue="intel")

    # If you sort descending, alert2 should appear first
    get = client_valid_access_token.get("/api/alert/?sort=queue|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending, alert1 should appear first
    get = client_valid_access_token.get("/api/alert/?sort=queue|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)


def test_get_sort_by_type(client_valid_access_token, db):
    alert_tree1 = helpers.create_alert(db, alert_type="type1")
    alert_tree2 = helpers.create_alert(db, alert_type="type2")

    # If you sort descending, alert2 should appear first
    get = client_valid_access_token.get("/api/alert/?sort=type|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree1.node_uuid)

    # If you sort ascending, alert1 should appear first
    get = client_valid_access_token.get("/api/alert/?sort=type|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["items"][1]["uuid"] == str(alert_tree2.node_uuid)


def test_get_alert_tree(client_valid_access_token, db):
    alert_tree = helpers.create_alert_from_json_file(db=db, json_path="/app/tests/alerts/small.json")

    # The small.json alert has 14 observables and 8 analyses. However, it only has two root observables.
    get = client_valid_access_token.get(f"/api/alert/{alert_tree.node_uuid}")
    assert str(get.json()["children"]).count("'observable'") == 14
    assert str(get.json()["children"]).count("'analysis'") == 8
    assert len(get.json()["children"]) == 2
