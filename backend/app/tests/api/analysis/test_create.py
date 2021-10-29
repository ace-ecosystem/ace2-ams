import json
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
        ("analysis_module_type", 123),
        ("analysis_module_type", ""),
        ("analysis_module_type", "abc"),
        ("details", 123),
        ("details", ""),
        ("details", "abc"),
        ("details", []),
        ("error_message", 123),
        ("error_message", ""),
        ("stack_trace", 123),
        ("stack_trace", ""),
        ("summary", 123),
        ("summary", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
    ],
)
def test_create_invalid_fields(client_valid_access_token, key, value):
    create = client_valid_access_token.post("/api/analysis/", json={key: value})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key,value",
    INVALID_CREATE_FIELDS,
)
def test_create_invalid_node_fields(client_valid_access_token, key, value):
    create = client_valid_access_token.post("/api/analysis/", json={key: value})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, key):
    # Create an object
    create1_json = {"uuid": str(uuid.uuid4())}
    client_valid_access_token.post("/api/analysis/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/analysis/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_analysis_module_type(client_valid_access_token):
    create = client_valid_access_token.post("/api/analysis/", json={"analysis_module_type": str(uuid.uuid4())})
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_nonexistent_parent_observable_uuid(client_valid_access_token):
    create = client_valid_access_token.post("/api/analysis/", json={"parent_observable_uuid": str(uuid.uuid4())})
    assert create.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_create_nonexistent_node_fields(client_valid_access_token, key, value):
    create = client_valid_access_token.post("/api/analysis/", json={key: value})
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("details", None),
        ("details", "{}"),
        ("details", '{"foo": "bar"}'),
        ("error_message", None),
        ("error_message", "test"),
        ("stack_trace", None),
        ("stack_trace", "test"),
        ("summary", None),
        ("summary", "test"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client_valid_access_token, key, value):
    # Create the object
    create = client_valid_access_token.post("/api/analysis/", json={key: value})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details" and value:
        assert get.json()[key] == json.loads(value)
    else:
        assert get.json()[key] == value


def test_create_valid_analysis_module_type(client_valid_access_token):
    # Create an analysis module type
    analysis_module_type_uuid = str(uuid.uuid4())
    client_valid_access_token.post(
        "/api/analysis/module_type/", json={"uuid": analysis_module_type_uuid, "value": "test", "version": "1.0.0"}
    )

    # Use the analysis module type to create a new analysis
    create = client_valid_access_token.post("/api/analysis/", json={"analysis_module_type": analysis_module_type_uuid})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["analysis_module_type"]["uuid"] == analysis_module_type_uuid


def test_create_valid_parent_observable_uuid(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

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
    observable_create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert observable_create.status_code == status.HTTP_201_CREATED

    # Read the observable instance back to get its current version
    get_observable = client_valid_access_token.get(observable_create.headers["Content-Location"])
    initial_version = get_observable.json()["version"]

    # Use the observable instance as the parent for a new analysis
    child_analysis_uuid = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/analysis/",
        json={
            "parent_observable_uuid": observable_uuid,
            "uuid": child_analysis_uuid,
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["parent_observable_uuid"] == observable_uuid

    # Read the observable instance back. By creating the analysis and setting its parent_observable_uuid,
    # you should be able to read that observable instance back and see the analysis listed in its
    # performed_analysis_uuids list even though it was not explictly added.
    get_observable = client_valid_access_token.get(observable_create.headers["Content-Location"])
    assert get_observable.json()["performed_analysis_uuids"] == [child_analysis_uuid]

    # Additionally, adding the child analysis to the observable instance should trigger the observable instance
    # to get a new version.
    assert get_observable.json()["version"] != initial_version


def test_create_valid_required_fields(client_valid_access_token):
    # Create the object
    create = client_valid_access_token.post("/api/analysis/", json={})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back, but since there are no required fields to create the analysis, there is nothing to verify.
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == 200


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_create_valid_node_directives(client_valid_access_token, values):
    # Create the directives. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/directive/", json={"value": value})

    # Create the node
    create = client_valid_access_token.post("/api/analysis/", json={"directives": values})
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

    # Create the node
    create = client_valid_access_token.post("/api/analysis/", json={"tags": values})
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

    # Create the node
    create = client_valid_access_token.post("/api/analysis/", json={"threat_actor": value})
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

    # Create the node
    create = client_valid_access_token.post("/api/analysis/", json={"threats": values})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(list(set(values)))
