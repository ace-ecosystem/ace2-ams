import pytest
import uuid

from fastapi import status

from tests.api.node import (
    INVALID_CREATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTOR,
    VALID_THREATS,
)


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", 123),
        ("description", ""),
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
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
    ],
)
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {"queue": "test_queue", "type": "test_type"}
    create_json[key] = value
    create = client_valid_access_token.post("/api/alert/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in create.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_CREATE_FIELDS,
)
def test_create_invalid_node_fields(client_valid_access_token, key, value):
    create = client_valid_access_token.post(
        "/api/alert/", json={key: value, "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, key):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an object
    create1_json = {"uuid": str(uuid.uuid4()), "queue": "test_queue", "type": "test_type"}
    client_valid_access_token.post("/api/alert/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"queue": "test_queue", "type": "test_type"}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/alert/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_owner(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an object
    create = client_valid_access_token.post(
        "/api/alert/", json={"owner": "johndoe", "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "user" in create.text


def test_create_nonexistent_queue(client_valid_access_token):
    # Create an alert type
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an object
    create = client_valid_access_token.post("/api/alert/", json={"queue": "test_queue", "type": "test_type"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "alert_queue" in create.text


def test_create_nonexistent_tool(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an object
    create = client_valid_access_token.post(
        "/api/alert/", json={"tool": "abc", "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "alert_tool" in create.text


def test_create_nonexistent_tool_instance(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an object
    create = client_valid_access_token.post(
        "/api/alert/", json={"tool_instance": "abc", "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "alert_tool_instance" in create.text


def test_create_nonexistent_type(client_valid_access_token):
    # Create an alert type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create an object
    create = client_valid_access_token.post("/api/alert/", json={"queue": "test_queue", "type": "test_type"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "alert_type" in create.text


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_create_nonexistent_node_fields(client_valid_access_token, key, value):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    create = client_valid_access_token.post(
        "/api/alert/", json={key: value, "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", None),
        ("description", "test"),
        ("event_time", 1640995200),
        ("event_time", "2022-01-01T00:00:00Z"),
        ("event_time", "2022-01-01 00:00:00"),
        ("event_time", "2022-01-01 00:00:00.000000"),
        ("event_time", "2021-12-31 19:00:00-05:00"),
        ("instructions", None),
        ("instructions", "test"),
        ("name", None),
        ("name", "test"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client_valid_access_token, key, value):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create the object
    create = client_valid_access_token.post(
        "/api/alert/", json={key: value, "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for event_time, make sure that the retrieved value matches the proper UTC timestamp
    if key == "event_time" and value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == value


def test_create_valid_owner(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

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

    # Use the user to create a new alert
    create = client_valid_access_token.post(
        "/api/alert/", json={"owner": "johndoe", "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["owner"]["username"] == "johndoe"


def test_create_valid_tool(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert tool
    client_valid_access_token.post("/api/alert/tool/", json={"value": "test_tool"})

    # Use the tool to create a new alert
    create = client_valid_access_token.post(
        "/api/alert/", json={"tool": "test_tool", "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tool"]["value"] == "test_tool"


def test_create_valid_tool_instance(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create an alert tool instance
    client_valid_access_token.post("/api/alert/tool/instance/", json={"value": "test_tool_instance"})

    # Use the tool instance to create a new alert
    create = client_valid_access_token.post(
        "/api/alert/", json={"tool_instance": "test_tool_instance", "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tool_instance"]["value"] == "test_tool_instance"


def test_create_valid_required_fields(client_valid_access_token):
    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create the object
    create = client_valid_access_token.post("/api/alert/", json={"queue": "test_queue", "type": "test_type"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["queue"]["value"] == "test_queue"
    assert get.json()["type"]["value"] == "test_type"


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_create_valid_node_directives(client_valid_access_token, values):
    # Create the directives. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/directive/", json={"value": value})

    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create the node
    create = client_valid_access_token.post(
        "/api/alert/", json={"directives": values, "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["directives"]) == len(list(set(values)))


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_create_valid_node_tags(client_valid_access_token, values):
    # Create the tags. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/tag/", json={"value": value})

    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create the node
    create = client_valid_access_token.post(
        "/api/alert/", json={"tags": values, "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["tags"]) == len(list(set(values)))


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_create_valid_node_threat_actor(client_valid_access_token, value):
    # Create the threat actor. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    if value:
        client_valid_access_token.post("/api/node/threat_actor/", json={"value": value})

    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create the node
    create = client_valid_access_token.post(
        "/api/analysis/", json={"threat_actor": value, "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    if value:
        assert get.json()["threat_actor"]["value"] == value
    else:
        assert get.json()["threat_actor"] is None


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_create_valid_node_threats(client_valid_access_token, values):
    # Create a threat type
    client_valid_access_token.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create the threats. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/threat/", json={"types": ["test_type"], "value": value})

    # Create an alert queue and type
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})
    client_valid_access_token.post("/api/alert/type/", json={"value": "test_type"})

    # Create the node
    create = client_valid_access_token.post(
        "/api/analysis/", json={"threats": values, "queue": "test_queue", "type": "test_type"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(list(set(values)))
