import pytest
import uuid

from fastapi import status
from db.schemas.observable import Observable

from tests.api.node import (
    INVALID_CREATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTOR,
    VALID_THREATS,
)
from tests import helpers


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("context", 123),
        ("context", ""),
        ("expires_on", ""),
        ("expires_on", "Monday"),
        ("expires_on", "2022-01-01"),
        ("for_detection", 123),
        ("for_detection", None),
        ("for_detection", "True"),
        ("redirection_uuid", 123),
        ("redirection_uuid", ""),
        ("redirection_uuid", "abc"),
        ("time", None),
        ("time", ""),
        ("time", "Monday"),
        ("time", "2022-01-01"),
        ("type", 123),
        ("type", None),
        ("type", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("uuid", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {
        "node_tree": {"root_node_uuid": str(uuid.uuid4())},
        "type": "test_type",
        "value": "test",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/", json=[create_json])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(create.json()["detail"]) == 1
    assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key,value",
    INVALID_CREATE_FIELDS,
)
def test_create_invalid_node_fields(client_valid_access_token, key, value):
    create_json = {
        key: value,
        "node_tree": {"root_node_uuid": str(uuid.uuid4())},
        "type": "test_type",
        "value": "test",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/", json=[create_json])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(create.json()["detail"]) == 1
    assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, db, key):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an object
    create1_json = {
        "node_tree": {"root_node_uuid": str(alert.uuid)},
        "type": "test_type",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    client_valid_access_token.post("/api/observable/", json=[create1_json])

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"node_tree": {"root_node_uuid": str(alert.uuid)}, "type": "test_type", "value": "test2"}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/observable/", json=[create2_json])
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_duplicate_type_value(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an object
    client_valid_access_token.post(
        "/api/observable/",
        json=[{"node_tree": {"root_node_uuid": str(alert.uuid)}, "type": "test_type", "value": "test"}],
    )

    # Ensure you cannot create another observable with the same type+value combination in the same node tree location
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[{"node_tree": {"root_node_uuid": str(alert.uuid)}, "type": "test_type", "value": "test"}],
    )

    assert create.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("type"),
        ("value"),
    ],
)
def test_create_missing_required_fields(client_valid_access_token, key):
    create_json = {"type": "test_type", "value": "test"}
    del create_json[key]
    create = client_valid_access_token.post("/api/observable/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_alert(client_valid_access_token, db):
    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    nonexistent_uuid = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[{"node_tree": {"root_node_uuid": nonexistent_uuid}, "type": "test_type", "value": "test"}],
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert nonexistent_uuid in create.text


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_create_nonexistent_node_fields(client_valid_access_token, db, key, value):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Ensure you cannot create an observable instance with a nonexistent type
    create_json = {
        "node_tree": {"root_node_uuid": str(alert.uuid)},
        "type": "test_type",
        "value": "test",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_nonexistent_redirection(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    nonexistent_uuid = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                "node_tree": {"root_node_uuid": str(alert.uuid)},
                "redirection_uuid": nonexistent_uuid,
                "type": "test_type",
                "value": "test",
            }
        ],
    )

    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert nonexistent_uuid in create.text


def test_create_nonexistent_type(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)

    nonexistent_type = "test_type"
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[{"node_tree": {"root_node_uuid": str(alert.uuid)}, "type": nonexistent_type, "value": "test"}],
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert nonexistent_type in create.text


#
# VALID TESTS
#


def test_create_bulk(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)
    initial_alert_version = alert.version

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create some observables
    observables = []
    for i in range(3):
        observables.append(
            {
                "node_tree": {"root_node_uuid": str(alert.uuid)},
                "type": "test_type",
                "value": f"test{i}",
            }
        )
    create = client_valid_access_token.post("/api/observable/", json=observables)
    assert create.status_code == status.HTTP_201_CREATED

    # Their should be 3 observables in the database
    observables = db.query(Observable).all()
    assert len(observables) == 3

    # Additionally, creating an observable should trigger the alert to get a new version.
    assert alert.version != initial_alert_version


@pytest.mark.parametrize(
    "key,value",
    [
        ("context", None),
        ("context", "test"),
        ("expires_on", None),
        ("expires_on", 1640995200),
        ("expires_on", "2022-01-01T00:00:00Z"),
        ("expires_on", "2022-01-01 00:00:00"),
        ("expires_on", "2022-01-01 00:00:00.000000"),
        ("expires_on", "2021-12-31 19:00:00-05:00"),
        ("for_detection", False),
        ("for_detection", True),
        ("time", 1640995200),
        ("time", "2022-01-01T00:00:00Z"),
        ("time", "2022-01-01 00:00:00"),
        ("time", "2022-01-01 00:00:00.000000"),
        ("time", "2021-12-31 19:00:00-05:00"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client_valid_access_token, db, key, value):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create the object
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[{key: value, "node_tree": {"root_node_uuid": str(alert.uuid)}, "type": "test_type", "value": "test"}],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if (key == "expires_on" or key == "time") and value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == value


def test_create_valid_redirection(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an observable
    observable_uuid = str(uuid.uuid4())
    create_json = {
        "node_tree": {"root_node_uuid": str(alert.uuid)},
        "type": "test_type",
        "uuid": observable_uuid,
        "value": "test",
    }
    client_valid_access_token.post("/api/observable/", json=[create_json])

    # Create another observable that redirects to the previously created one
    create_json = {
        "node_tree": {"root_node_uuid": str(alert.uuid)},
        "redirection_uuid": observable_uuid,
        "type": "test_type",
        "value": "test2",
    }
    create = client_valid_access_token.post("/api/observable/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["redirection_uuid"] == observable_uuid


def test_create_valid_required_fields(client_valid_access_token, db):
    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create the object
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[{"node_tree": {"root_node_uuid": str(alert.uuid)}, "type": "test_type", "value": "test"}],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_create_valid_node_directives(client_valid_access_token, db, values):
    # Create the directives
    for value in values:
        helpers.create_node_directive(value=value, db=db)

    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an observable instance
    create_json = {
        "node_tree": {"root_node_uuid": str(alert.uuid)},
        "type": "test_type",
        "value": "test",
        "directives": values,
    }
    create = client_valid_access_token.post("/api/observable/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["directives"]) == len(set(values))


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_create_valid_node_tags(client_valid_access_token, db, values):
    # Create the tags
    for value in values:
        helpers.create_node_tag(value=value, db=db)

    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an observable instance
    create_json = {
        "node_tree": {"root_node_uuid": str(alert.uuid)},
        "type": "test_type",
        "value": "test",
        "tags": values,
    }
    create = client_valid_access_token.post("/api/observable/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["tags"]) == len(list(set(values)))


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_create_valid_node_threat_actor(client_valid_access_token, db, value):
    # Create the threat actor
    if value:
        helpers.create_node_threat_actor(value=value, db=db)

    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an observable instance
    create_json = {
        "node_tree": {"root_node_uuid": str(alert.uuid)},
        "type": "test_type",
        "value": "test",
        "threat_actor": value,
    }
    create = client_valid_access_token.post("/api/observable/", json=[create_json])
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
def test_create_valid_node_threats(client_valid_access_token, db, values):
    # Create the threats
    for value in values:
        helpers.create_node_threat(value=value, db=db)

    # Create an alert
    alert = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an observable instance
    create_json = {
        "node_tree": {"root_node_uuid": str(alert.uuid)},
        "type": "test_type",
        "value": "test",
        "threats": values,
    }
    create = client_valid_access_token.post("/api/observable/", json=[create_json])
    print(create.text)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(set(values))
