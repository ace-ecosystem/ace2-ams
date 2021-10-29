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
from tests.helpers import create_alert


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("alert_uuid", 123),
        ("alert_uuid", None),
        ("alert_uuid", ""),
        ("alert_uuid", "abc"),
        ("context", 123),
        ("context", ""),
        ("parent_analysis_uuid", 123),
        ("parent_analysis_uuid", None),
        ("parent_analysis_uuid", ""),
        ("parent_analysis_uuid", "abc"),
        ("performed_analysis_uuids", 123),
        ("performed_analysis_uuids", "abc"),
        ("performed_analysis_uuids", [123]),
        ("performed_analysis_uuids", [None]),
        ("performed_analysis_uuids", [""]),
        ("performed_analysis_uuids", ["abc"]),
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
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {
        key: value,
        "alert_uuid": str(uuid.uuid4()),
        "parent_analysis_uuid": str(uuid.uuid4()),
        "type": "test_type",
        "value": "test",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in create.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_CREATE_FIELDS,
)
def test_create_invalid_node_fields(client_valid_access_token, key, value):
    create_json = {
        key: value,
        "alert_uuid": str(uuid.uuid4()),
        "parent_analysis_uuid": str(uuid.uuid4()),
        "type": "test_type",
        "value": "test",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_duplicate_uuid(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an object
    create_json = {
        "uuid": str(uuid.uuid4()),
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
    }
    client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Ensure you cannot create another object with the same UUID
    create2 = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_alert(client_valid_access_token):
    # Create an alert
    _, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)
    alert_uuid = str(uuid.uuid4())

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Ensure you cannot create an observable instance with a nonexistent alert
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert alert_uuid in create.text


def test_create_nonexistent_analysis(client_valid_access_token):
    # Create an alert
    alert_uuid, _ = create_alert(client_valid_access_token=client_valid_access_token)
    analysis_uuid = str(uuid.uuid4())

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Ensure you cannot create an observable instance with a nonexistent analysis
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert analysis_uuid in create.text


def test_create_nonexistent_performed_analysis(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Ensure you cannot create an observable instance with a nonexistent performed analysis
    performed_analysis_uuid = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "performed_analysis_uuids": [performed_analysis_uuid],
        "type": "test_type",
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert performed_analysis_uuid in create.text


def test_create_nonexistent_redirection(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Ensure you cannot create an observable instance with a nonexistent redirection target
    redirection_uuid = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "redirection_uuid": redirection_uuid,
        "type": "test_type",
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert redirection_uuid in create.text


def test_create_nonexistent_type(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Ensure you cannot create an observable instance with a nonexistent type
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "abc",
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in create.text


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_create_nonexistent_node_fields(client_valid_access_token, key, value):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Ensure you cannot create an observable instance with a nonexistent type
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_create_bulk(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Read the alert back to get its current version
    # TODO: Fix this hardcoded URL
    get_alert = client_valid_access_token.get(f"http://testserver/api/alert/{alert_uuid}")
    initial_alert_version = get_alert.json()["version"]

    # Read the analysis back to get its current version
    # TODO: Fix this hardcoded URL
    get_analysis = client_valid_access_token.get(f"http://testserver/api/analysis/{analysis_uuid}")
    initial_analysis_version = get_analysis.json()["version"]

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create some observable instances
    observable_instances = []
    for i in range(3):
        observable_uuid = str(uuid.uuid4())
        observable_instances.append(
            {
                "alert_uuid": alert_uuid,
                "parent_analysis_uuid": analysis_uuid,
                "type": "test_type",
                "uuid": observable_uuid,
                "value": f"test{i}",
            }
        )
    create = client_valid_access_token.post("/api/observable/instance/", json=observable_instances)
    assert create.status_code == status.HTTP_201_CREATED

    # Read the parent analysis back. There should be 3 discovered observable instance UUIDs.
    # TODO: Fix this hardcoded URL
    get_analysis = client_valid_access_token.get(f"http://testserver/api/analysis/{analysis_uuid}")
    assert len(get_analysis.json()["discovered_observable_uuids"]) == 3

    # Additionally, creating an observable instance should trigger the alert and analysis to get a new version.
    # TODO: Fix this hardcoded URL
    get_alert = client_valid_access_token.get(f"http://testserver/api/alert/{alert_uuid}")
    assert get_alert.json()["version"] != initial_alert_version
    assert get_analysis.json()["version"] != initial_analysis_version


@pytest.mark.parametrize(
    "key,value",
    [
        ("context", None),
        ("context", "test"),
        ("time", 1640995200),
        ("time", "2022-01-01T00:00:00Z"),
        ("time", "2022-01-01 00:00:00"),
        ("time", "2022-01-01 00:00:00.000000"),
        ("time", "2021-12-31 19:00:00-05:00"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client_valid_access_token, key, value):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create the observable instance
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for time, make sure that the retrieved value matches the proper UTC timestamp
    if key == "time" and value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == value


def test_create_valid_performed_analysis_uuids(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create a child analysis for the observable instance
    child_analysis_uuid = str(uuid.uuid4())
    analysis_create = client_valid_access_token.post("/api/analysis/", json={"uuid": child_analysis_uuid})

    # Read the analysis back to get its current version
    get_analysis = client_valid_access_token.get(analysis_create.headers["Content-Location"])
    initial_version = get_analysis.json()["version"]

    # Create the observable instance
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "performed_analysis_uuids": [child_analysis_uuid],
        "type": "test_type",
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["performed_analysis_uuids"] == [child_analysis_uuid]

    # Read the analysis back. By creating the observable instance and setting its performed_analysis_uuids, you should
    # be able to read the analysis back and see the observable instance listed as its parent_observable_uuid even
    # though it was not explicitly added.
    get_analysis = client_valid_access_token.get(analysis_create.headers["Content-Location"])
    assert get_analysis.json()["parent_observable_uuid"] == get.json()["uuid"]

    # Additionally, adding the observable instance as the parent should trigger the analysis to have a new version.
    assert get_analysis.json()["version"] != initial_version


def test_create_valid_redirection(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    observable_instance_uuid = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "uuid": observable_instance_uuid,
        "value": "test",
    }
    client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Create another observable instance that redirects to the previously created one
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "redirection_uuid": observable_instance_uuid,
        "type": "test_type",
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["redirection_uuid"] == observable_instance_uuid


def test_create_valid_required_fields(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Read the alert back to get its current version
    # TODO: Fix this hardcoded URL
    get_alert = client_valid_access_token.get(f"http://testserver/api/alert/{alert_uuid}")
    initial_alert_version = get_alert.json()["version"]

    # Read the analysis back to get its current version
    # TODO: Fix this hardcoded URL
    get_analysis = client_valid_access_token.get(f"http://testserver/api/analysis/{analysis_uuid}")
    initial_analysis_version = get_analysis.json()["version"]

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    observable_uuid = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "uuid": observable_uuid,
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["alert_uuid"] == alert_uuid
    assert get.json()["parent_analysis_uuid"] == analysis_uuid
    assert get.json()["observable"]["type"]["value"] == "test_type"
    assert get.json()["uuid"] == observable_uuid
    assert get.json()["observable"]["value"] == "test"

    # Read the parent analysis back. You should see this observable instance in its discovered_observable_uuids list
    # even though it was not explicitly added.
    # TODO: Fix this hardcoded URL
    get_analysis = client_valid_access_token.get(f"http://testserver/api/analysis/{analysis_uuid}")
    assert get_analysis.json()["discovered_observable_uuids"] == [observable_uuid]

    # Additionally, creating an observable instance should trigger the alert and analysis to get a new version.
    # TODO: Fix this hardcoded URL
    get_alert = client_valid_access_token.get(f"http://testserver/api/alert/{alert_uuid}")
    assert get_alert.json()["version"] != initial_alert_version
    assert get_analysis.json()["version"] != initial_analysis_version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_create_valid_node_directives(client_valid_access_token, values):
    # Create the directives. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/directive/", json={"value": value})

    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "directives": values,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
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

    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "tags": values,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
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

    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "threat_actor": value,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
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

    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "threats": values,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(list(set(values)))
