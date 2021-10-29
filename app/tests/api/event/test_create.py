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
        ("alert_time", ""),
        ("alert_time", "Monday"),
        ("alert_time", "2022-01-01"),
        ("contain_time", ""),
        ("contain_time", "Monday"),
        ("contain_time", "2022-01-01"),
        ("disposition_time", ""),
        ("disposition_time", "Monday"),
        ("disposition_time", "2022-01-01"),
        ("event_time", ""),
        ("event_time", "Monday"),
        ("event_time", "2022-01-01"),
        ("name", 123),
        ("name", None),
        ("name", ""),
        ("owner", 123),
        ("owner", ""),
        ("ownership_time", ""),
        ("ownership_time", "Monday"),
        ("ownership_time", "2022-01-01"),
        ("prevention_tools", None),
        ("prevention_tools", "test_type"),
        ("prevention_tools", [123]),
        ("prevention_tools", [None]),
        ("prevention_tools", [""]),
        ("prevention_tools", ["abc", 123]),
        ("remediation_time", ""),
        ("remediation_time", "Monday"),
        ("remediation_time", "2022-01-01"),
        ("remediations", None),
        ("remediations", "test_type"),
        ("remediations", [123]),
        ("remediations", [None]),
        ("remediations", [""]),
        ("remediations", ["abc", 123]),
        ("risk_level", 123),
        ("risk_level", ""),
        ("source", 123),
        ("source", ""),
        ("status", 123),
        ("status", None),
        ("status", ""),
        ("type", 123),
        ("type", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("vectors", None),
        ("vectors", "test_type"),
        ("vectors", [123]),
        ("vectors", [None]),
        ("vectors", [""]),
        ("vectors", ["abc", 123]),
    ],
)
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {"name": "test", "status": "OPEN"}
    create_json[key] = value
    create = client_valid_access_token.post("/api/event/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in create.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_CREATE_FIELDS,
)
def test_create_invalid_node_fields(client_valid_access_token, key, value):
    create = client_valid_access_token.post("/api/event/", json={key: value, "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, key):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an object
    create1_json = {"uuid": str(uuid.uuid4()), "name": "test", "status": "OPEN"}
    client_valid_access_token.post("/api/event/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"name": "test2", "status": "OPEN"}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/event/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_owner(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an object
    create = client_valid_access_token.post("/api/event/", json={"owner": "johndoe", "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "user" in create.text


def test_create_nonexistent_prevention_tools(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an object
    create = client_valid_access_token.post(
        "/api/event/", json={"prevention_tools": ["test"], "name": "test", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_prevention_tool" in create.text


def test_create_nonexistent_remediations(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an object
    create = client_valid_access_token.post(
        "/api/event/", json={"remediations": ["test"], "name": "test", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_remediation" in create.text


def test_create_nonexistent_risk_level(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an object
    create = client_valid_access_token.post(
        "/api/event/", json={"risk_level": "test", "name": "test", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_risk_level" in create.text


def test_create_nonexistent_source(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an object
    create = client_valid_access_token.post("/api/event/", json={"source": "test", "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_source" in create.text


def test_create_nonexistent_status(client_valid_access_token):
    # Create an object
    create = client_valid_access_token.post("/api/event/", json={"name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_status" in create.text


def test_create_nonexistent_type(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an object
    create = client_valid_access_token.post("/api/event/", json={"type": "test", "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_type" in create.text


def test_create_nonexistent_vectors(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an object
    create = client_valid_access_token.post("/api/event/", json={"vectors": ["test"], "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_vector" in create.text


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_create_nonexistent_node_fields(client_valid_access_token, key, value):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    create = client_valid_access_token.post("/api/event/", json={key: value, "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("alert_time", None),
        ("alert_time", 1640995200),
        ("alert_time", "2022-01-01T00:00:00Z"),
        ("alert_time", "2022-01-01 00:00:00"),
        ("alert_time", "2022-01-01 00:00:00.000000"),
        ("alert_time", "2021-12-31 19:00:00-05:00"),
        ("contain_time", None),
        ("contain_time", 1640995200),
        ("contain_time", "2022-01-01T00:00:00Z"),
        ("contain_time", "2022-01-01 00:00:00"),
        ("contain_time", "2022-01-01 00:00:00.000000"),
        ("contain_time", "2021-12-31 19:00:00-05:00"),
        ("disposition_time", None),
        ("disposition_time", 1640995200),
        ("disposition_time", "2022-01-01T00:00:00Z"),
        ("disposition_time", "2022-01-01 00:00:00"),
        ("disposition_time", "2022-01-01 00:00:00.000000"),
        ("disposition_time", "2021-12-31 19:00:00-05:00"),
        ("event_time", None),
        ("event_time", 1640995200),
        ("event_time", "2022-01-01T00:00:00Z"),
        ("event_time", "2022-01-01 00:00:00"),
        ("event_time", "2022-01-01 00:00:00.000000"),
        ("event_time", "2021-12-31 19:00:00-05:00"),
        ("ownership_time", None),
        ("ownership_time", 1640995200),
        ("ownership_time", "2022-01-01T00:00:00Z"),
        ("ownership_time", "2022-01-01 00:00:00"),
        ("ownership_time", "2022-01-01 00:00:00.000000"),
        ("ownership_time", "2021-12-31 19:00:00-05:00"),
        ("remediation_time", None),
        ("remediation_time", 1640995200),
        ("remediation_time", "2022-01-01T00:00:00Z"),
        ("remediation_time", "2022-01-01 00:00:00"),
        ("remediation_time", "2022-01-01 00:00:00.000000"),
        ("remediation_time", "2021-12-31 19:00:00-05:00"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client_valid_access_token, key, value):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create the object
    create = client_valid_access_token.post("/api/event/", json={key: value, "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for one of the times, make sure that the retrieved value matches the proper UTC timestamp
    if key.endswith("_time") and value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == value


def test_create_valid_owner(client_valid_access_token):
    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

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

    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Use the user to create a new event
    create = client_valid_access_token.post("/api/event/", json={"owner": "johndoe", "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["owner"]["username"] == "johndoe"


def test_create_valid_prevention_tools(client_valid_access_token):
    # Create an event status and prevention tool
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})
    client_valid_access_token.post("/api/event/prevention_tool/", json={"value": "test"})

    # Use the prevention tool to create a new event
    create = client_valid_access_token.post(
        "/api/event/", json={"prevention_tools": ["test"], "name": "test", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["prevention_tools"][0]["value"] == "test"


def test_create_valid_remediations(client_valid_access_token):
    # Create an event status and remediation
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})
    client_valid_access_token.post("/api/event/remediation/", json={"value": "test"})

    # Use the remediation to create a new event
    create = client_valid_access_token.post(
        "/api/event/", json={"remediations": ["test"], "name": "test", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["remediations"][0]["value"] == "test"


def test_create_valid_risk_level(client_valid_access_token):
    # Create an event status and risk level
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})
    client_valid_access_token.post("/api/event/risk_level/", json={"value": "test"})

    # Use the risk level to create a new event
    create = client_valid_access_token.post(
        "/api/event/", json={"risk_level": "test", "name": "test", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["risk_level"]["value"] == "test"


def test_create_valid_source(client_valid_access_token):
    # Create an event status and source
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})
    client_valid_access_token.post("/api/event/source/", json={"value": "test"})

    # Use the source to create a new event
    create = client_valid_access_token.post("/api/event/", json={"source": "test", "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["source"]["value"] == "test"


def test_create_valid_type(client_valid_access_token):
    # Create an event status and type
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})
    client_valid_access_token.post("/api/event/type/", json={"value": "test"})

    # Use the type to create a new event
    create = client_valid_access_token.post("/api/event/", json={"type": "test", "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["type"]["value"] == "test"


def test_create_valid_vectors(client_valid_access_token):
    # Create an event status and vector
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})
    client_valid_access_token.post("/api/event/vector/", json={"value": "test"})

    # Use the vector to create a new event
    create = client_valid_access_token.post("/api/event/", json={"vectors": ["test"], "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["vectors"][0]["value"] == "test"


def test_create_valid_required_fields(client_valid_access_token):
    # Create an event status and remediation
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create the object
    create = client_valid_access_token.post("/api/event/", json={"name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["name"] == "test"
    assert get.json()["status"]["value"] == "OPEN"


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_create_valid_node_directives(client_valid_access_token, values):
    # Create the directives. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/directive/", json={"value": value})

    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create the node
    create = client_valid_access_token.post(
        "/api/event/", json={"directives": values, "name": "test", "status": "OPEN"}
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

    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create the node
    create = client_valid_access_token.post("/api/event/", json={"tags": values, "name": "test", "status": "OPEN"})
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

    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create the node
    create = client_valid_access_token.post(
        "/api/event/", json={"threat_actor": value, "name": "test", "status": "OPEN"}
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

    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create the node
    create = client_valid_access_token.post("/api/event/", json={"threats": values, "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(list(set(values)))
