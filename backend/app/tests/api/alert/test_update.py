import pytest
import uuid

from fastapi import status

from tests.api.node import (
    INVALID_UPDATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTOR,
    VALID_THREATS,
)
from tests.helpers import create_test_user


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", 123),
        ("description", ""),
        ("disposition", 123),
        ("disposition", ""),
        ("event_uuid", 123),
        ("event_uuid", ""),
        ("event_uuid", "abc"),
        ("event_time", None),
        ("event_time", ""),
        ("event_time", "Monday"),
        ("event_time", "2022-01-01"),
        ("instructions", 123),
        ("instructions", ""),
        ("name", 123),
        ("name", ""),
        ("owner", 123),
        ("owner", ""),
        ("queue", 123),
        ("queue", None),
        ("queue", ""),
        ("tool", 123),
        ("tool", ""),
        ("tool_instance", 123),
        ("tool_instance", ""),
        ("type", 123),
        ("type", None),
        ("type", ""),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/alert/{uuid.uuid4()}", json={key: value, "version": str(uuid.uuid4())}
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_UPDATE_FIELDS,
)
def test_update_invalid_node_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/alert/{uuid.uuid4()}", json={"version": str(uuid.uuid4()), key: value}
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/alert/1", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    create = client_valid_access_token.post("/api/alert/", json={"queue": "test_queue", "type": "test_type"})

    # Make sure you cannot update it using an invalid version
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key,value",
    [
        ("disposition", "abc"),
        ("event_uuid", str(uuid.uuid4())),
        ("owner", "johndoe"),
        ("queue", "abc"),
        ("tool", "abc"),
        ("tool_instance", "abc"),
        ("type", "abc"),
    ],
)
def test_update_nonexistent_fields(client_valid_access_token, key, value):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Make sure you cannot update it to use a nonexistent field value
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: value, "version": version})
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_update_nonexistent_node_fields(client_valid_access_token, key, value):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: value, "version": version})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/alert/{uuid.uuid4()}", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_disposition(client_valid_access_token, db):
    # Create an analyst user
    create_test_user(db=db, username="analyst", password="asdfasdf")

    # Create an alert type
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["disposition"] is None

    # Create a disposition
    client_valid_access_token.post("/api/alert/disposition/", json={"rank": 1, "value": "test"})

    # Update the disposition
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"disposition": "test", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["disposition"]["value"] == "test"
    assert get.json()["version"] != version


def test_update_event_uuid(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["event_uuid"] is None

    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    event_uuid = str(uuid.uuid4())
    initial_event_version = str(uuid.uuid4())
    event_create = client_valid_access_token.post(
        "/api/event/",
        json={
            "version": initial_event_version,
            "name": "test",
            "status": "OPEN",
            "uuid": event_uuid,
        },
    )

    # Update the alert to add it to the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"event_uuid": event_uuid, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["event_uuid"] == event_uuid
    assert get.json()["version"] != version

    # Read the event back. By adding the alert to the event, you should be able to see the alert UUID in the event's
    # alert_uuids list even though it was not explicitly added.
    get_event = client_valid_access_token.get(event_create.headers["Content-Location"])
    assert get_event.json()["alert_uuids"] == [get.json()["uuid"]]

    # Additionally, adding the alert to the event should trigger the event to have a new version.
    assert get_event.json()["version"] != initial_event_version


def test_update_owner(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["owner"] is None

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create a user
    create_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    client_valid_access_token.post("/api/user/", json=create_json)

    # Update the owner
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"owner": "johndoe", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["owner"]["username"] == "johndoe"
    assert get.json()["version"] != version


def test_update_queue(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["queue"]["value"] == "test_queue"

    # Create a new alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue2"})

    # Update the disposition
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"queue": "test_queue2", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["queue"]["value"] == "test_queue2"
    assert get.json()["version"] != version


def test_update_tool(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tool"] is None

    # Create an alert tool
    client_valid_access_token.post("/api/alert/tool/", json={"value": "test"})

    # Update the tool
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"tool": "test", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tool"]["value"] == "test"
    assert get.json()["version"] != version


def test_update_tool_instance(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tool_instance"] is None

    # Create an alert tool instance
    client_valid_access_token.post("/api/alert/tool/instance/", json={"value": "test"})

    # Update the tool instance
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"tool_instance": "test", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tool_instance"]["value"] == "test"
    assert get.json()["version"] != version


def test_update_type(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["type"]["value"] == "test_type"

    # Create a new alert type
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type2"})

    # Update the disposition
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"type": "test_type2", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["type"]["value"] == "test_type2"
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_update_valid_node_directives(client_valid_access_token, values):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["directives"] == []

    # Create the directives. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/directive/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"directives": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["directives"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_update_valid_node_tags(client_valid_access_token, values):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tags"] == []

    # Create the tags. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/tag/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"tags": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["tags"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_update_valid_node_threat_actor(client_valid_access_token, value):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["threat_actor"] is None

    # Create the threat actor
    if value:
        client_valid_access_token.post("/api/node/threat_actor/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"threat_actor": value, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    if value:
        assert get.json()["threat_actor"]["value"] == value
    else:
        assert get.json()["threat_actor"] is None

    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_update_valid_node_threats(client_valid_access_token, values):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert
    version = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/alert/", json={"version": version, "queue": "test_queue", "type": "test_type"}
    )

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["directives"] == []

    # Create a threat type
    client_valid_access_token.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create the threats. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/threat/", json={"types": ["test_type"], "value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"threats": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", None),
        ("description", "test", "test"),
        ("event_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("instructions", None, "test"),
        ("instructions", "test", None),
        ("instructions", "test", "test"),
        ("name", None, "test"),
        ("name", "test", None),
        ("name", "test", "test"),
    ],
)
def test_update(client_valid_access_token, key, initial_value, updated_value):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create the object
    version = str(uuid.uuid4())
    create_json = {"version": version, "queue": "test_queue", "type": "test_type"}
    create_json[key] = initial_value
    create = client_valid_access_token.post("/api/alert/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == initial_value

    # Update it
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"version": version, key: updated_value}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for event_time, make sure that the retrieved value matches the proper UTC timestamp
    if key == "event_time":
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == updated_value

    assert get.json()["version"] != version
