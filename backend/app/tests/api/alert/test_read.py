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
    # Create some alerts
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
    # Create some alerts
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
    # Create some alerts
    helpers.create_alert(db)
    alert = helpers.create_alert(db, disposition_time=datetime.utcnow())
    helpers.create_alert(db, disposition_time=datetime.utcnow() + timedelta(seconds=5))

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by dispositioned_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"dispositioned_after": alert.disposition_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_dispositioned_before(client_valid_access_token, db):
    # Create some alerts
    helpers.create_alert(db)
    helpers.create_alert(db, disposition_time=datetime.utcnow() - timedelta(seconds=5))
    alert = helpers.create_alert(db, disposition_time=datetime.utcnow())

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by dispositioned_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"dispositioned_before": alert.disposition_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_after(client_valid_access_token, db):
    # Create some alerts
    alert = helpers.create_alert(db, event_time=datetime.utcnow())
    helpers.create_alert(db, event_time=datetime.utcnow() + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by event_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"event_time_after": alert.event_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_before(client_valid_access_token, db):
    # Create some alerts
    helpers.create_alert(db, event_time=datetime.utcnow())
    alert = helpers.create_alert(db, event_time=datetime.utcnow() + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by event_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"event_time_before": alert.event_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_uuid(client_valid_access_token, db):
    # Create an event
    event = helpers.create_event(name="Test Event", db=db)

    # Create some alerts
    helpers.create_alert(db)
    alert = helpers.create_alert(db)

    # Add one alert to the event
    alert.event_uuid = event.uuid

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the event_uuid
    get = client_valid_access_token.get(f"/api/alert/?event_uuid={event.uuid}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["event_uuid"] == str(event.uuid)


def test_get_filter_insert_time_after(client_valid_access_token, db):
    # Create some alerts
    alert = helpers.create_alert(db, insert_time=datetime.utcnow())
    helpers.create_alert(db, insert_time=datetime.utcnow() + timedelta(seconds=5))

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by insert_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"insert_time_after": alert.insert_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_insert_time_before(client_valid_access_token, db):
    # Create some alerts
    helpers.create_alert(db, insert_time=datetime.utcnow() - timedelta(seconds=5))
    alert = helpers.create_alert(db, insert_time=datetime.utcnow())

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by insert_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"insert_time_before": alert.insert_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_name(client_valid_access_token, db):
    # Create some alerts
    helpers.create_alert(db, name="Test Alert")
    helpers.create_alert(db, name="Some Other Alert")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the name
    get = client_valid_access_token.get("/api/alert/?name=test alert")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "Test Alert"


def test_get_filter_owner(client_valid_access_token, db):
    # Create an analyst user
    helpers.create_user(username="analyst", db=db)

    # Create some alerts
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
    # Create some alerts
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
    # Create some alerts
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


def test_get_filter_threats(client_valid_access_token, db):
    # Create some alerts
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
    # Create some alerts
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
    # Create some alerts
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
    # Create some alerts
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
    # Create some alerts
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
