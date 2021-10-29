import time
import uuid

from fastapi import status
from urllib.parse import urlencode

from tests.helpers import create_alert, create_event, create_test_user


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


def test_get_all_pagination(client_valid_access_token):
    # Create 11 alerts
    for _ in range(11):
        create_alert(client_valid_access_token)

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


def test_get_filter_disposition(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token)
    create_alert(client_valid_access_token, disposition="FALSE_POSITIVE")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the disposition
    get = client_valid_access_token.get("/api/alert/?disposition=none")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["disposition"] is None


def test_get_filter_disposition_user(client_valid_access_token, db):
    # Create an analyst user
    create_test_user(db=db, username="analyst", password="asdfasdf")

    # Create some alerts
    create_alert(client_valid_access_token)
    create_alert(client_valid_access_token, disposition="FALSE_POSITIVE")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the disposition user
    get = client_valid_access_token.get("/api/alert/?disposition_user=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["disposition_user"]["username"] == "analyst"


def test_get_filter_dispositioned_after(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token)
    alert_uuid, _ = create_alert(client_valid_access_token, disposition="FALSE_POSITIVE")
    time.sleep(0.25)
    create_alert(client_valid_access_token, disposition="FALSE_POSITIVE")

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # Get the disposition_time of the first dispositioned alert
    get = client_valid_access_token.get(f"/api/alert/{alert_uuid}")
    disposition_time = get.json()["disposition_time"]

    # There should only be 1 alert when we filter by dispositioned_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"dispositioned_after": disposition_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_dispositioned_before(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token)
    create_alert(client_valid_access_token, disposition="FALSE_POSITIVE")
    time.sleep(0.25)
    alert_uuid, _ = create_alert(client_valid_access_token, disposition="FALSE_POSITIVE")

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # Get the disposition_time of the second dispositioned alert
    get = client_valid_access_token.get(f"/api/alert/{alert_uuid}")
    disposition_time = get.json()["disposition_time"]

    # There should only be 1 alert when we filter by dispositioned_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"dispositioned_before": disposition_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_after(client_valid_access_token):
    # Create some alerts
    alert_uuid, _ = create_alert(client_valid_access_token)
    time.sleep(0.25)
    create_alert(client_valid_access_token)

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # Get the event_time of the first alert
    get = client_valid_access_token.get(f"/api/alert/{alert_uuid}")
    event_time = get.json()["event_time"]

    # There should only be 1 alert when we filter by event_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"event_time_after": event_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_time_before(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token)
    time.sleep(0.25)
    alert_uuid, _ = create_alert(client_valid_access_token)

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # Get the event_time of the second alert
    get = client_valid_access_token.get(f"/api/alert/{alert_uuid}")
    event_time = get.json()["event_time"]

    # There should only be 1 alert when we filter by event_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"event_time_before": event_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_event_uuid(client_valid_access_token):
    # Create an event
    event_uuid = create_event(client_valid_access_token, name="Test Event")

    # Create some alerts
    create_alert(client_valid_access_token)
    alert_uuid, _ = create_alert(client_valid_access_token)

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # Read one of the alerts back
    get = client_valid_access_token.get(f"/api/alert/{alert_uuid}")

    # Add one of the alerts to the event
    client_valid_access_token.patch(
        f"/api/alert/{alert_uuid}", json={"event_uuid": event_uuid, "version": get.json()["version"]}
    )

    # There should only be 1 alert when we filter by the event_uuid
    get = client_valid_access_token.get(f"/api/alert/?event_uuid={event_uuid}")
    print(get.json())
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["event_uuid"] == event_uuid


def test_get_filter_insert_time_after(client_valid_access_token):
    # Create some alerts
    alert_uuid, _ = create_alert(client_valid_access_token)
    time.sleep(0.25)
    create_alert(client_valid_access_token)

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # Get the insert_time of the first alert
    get = client_valid_access_token.get(f"/api/alert/{alert_uuid}")
    insert_time = get.json()["insert_time"]

    # There should only be 1 alert when we filter by insert_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"insert_time_after": insert_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_insert_time_before(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token)
    time.sleep(0.25)
    alert_uuid, _ = create_alert(client_valid_access_token)

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # Get the insert_time of the second alert
    get = client_valid_access_token.get(f"/api/alert/{alert_uuid}")
    insert_time = get.json()["insert_time"]

    # There should only be 1 alert when we filter by insert_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params = {"insert_time_before": insert_time}
    get = client_valid_access_token.get(f"/api/alert/?{urlencode(params)}")
    assert get.json()["total"] == 1


def test_get_filter_name(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token, name="Test Alert")
    create_alert(client_valid_access_token, name="Some Other Alert")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the name
    get = client_valid_access_token.get("/api/alert/?name=test alert")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "Test Alert"


def test_get_filter_owner(client_valid_access_token, db):
    # Create an analyst user
    create_test_user(db=db, username="analyst", password="asdfasdf")

    # Create some alerts
    create_alert(client_valid_access_token)
    create_alert(client_valid_access_token, owner="analyst")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the owner
    get = client_valid_access_token.get("/api/alert/?owner=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["owner"]["username"] == "analyst"


def test_get_filter_queue(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token, alert_queue="test_queue1")
    create_alert(client_valid_access_token, alert_queue="test_queue2")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the alert queue
    get = client_valid_access_token.get("/api/alert/?queue=test_queue1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["queue"]["value"] == "test_queue1"


def test_get_filter_tool(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token, tool="test_tool1")
    create_alert(client_valid_access_token, tool="test_tool2")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the tool
    get = client_valid_access_token.get("/api/alert/?tool=test_tool1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["tool"]["value"] == "test_tool1"


def test_get_filter_tool_instance(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token, tool_instance="test_tool_instance1")
    create_alert(client_valid_access_token, tool_instance="test_tool_instance2")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the tool
    get = client_valid_access_token.get("/api/alert/?tool_instance=test_tool_instance1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["tool_instance"]["value"] == "test_tool_instance1"


def test_get_filter_type(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token, alert_type="test_type")
    create_alert(client_valid_access_token, alert_type="test_type2")

    # There should be 2 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 2

    # There should only be 1 alert when we filter by the alert type
    get = client_valid_access_token.get("/api/alert/?type=test_type")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type"


def test_get_multiple_filters(client_valid_access_token):
    # Create some alerts
    create_alert(client_valid_access_token, alert_type="test_type1")
    create_alert(client_valid_access_token, alert_type="test_type1", disposition="FALSE_POSITIVE")
    create_alert(client_valid_access_token, alert_type="test_type2", disposition="FALSE_POSITIVE")

    # There should be 3 total alerts
    get = client_valid_access_token.get("/api/alert/")
    assert get.json()["total"] == 3

    # There should only be 1 alert when we filter by the alert type and disposition
    get = client_valid_access_token.get("/api/alert/?type=test_type1&disposition=FALSE_POSITIVE")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type1"
    assert get.json()["items"][0]["disposition"]["value"] == "FALSE_POSITIVE"
