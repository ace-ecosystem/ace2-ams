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
from tests import helpers


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
    create_json = {
        "node_tree": {"root_node_uuid": str(uuid.uuid4())},
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/analysis/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(create.json()["detail"]) == 1
    assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key,value",
    INVALID_CREATE_FIELDS,
)
def test_create_invalid_node_fields(client_valid_access_token, key, value):
    create = client_valid_access_token.post(
        "/api/analysis/",
        json={
            key: value,
            "node_tree": {"root_node_uuid": str(uuid.uuid4())},
        },
    )
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
    alert = helpers.create_alert(db=db)

    # Create an object
    create1_json = {"uuid": str(uuid.uuid4()), "node_tree": {"root_node_uuid": str(alert.uuid)}}
    client_valid_access_token.post("/api/analysis/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"node_tree": {"root_node_uuid": str(alert.uuid)}}
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/analysis/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_analysis_module_type(client_valid_access_token, db):
    alert = helpers.create_alert(db=db)

    create = client_valid_access_token.post(
        "/api/analysis/",
        json={"node_tree": {"root_node_uuid": str(alert.uuid)}, "analysis_module_type": str(uuid.uuid4())},
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_create_nonexistent_node_fields(client_valid_access_token, db, key, value):
    alert = helpers.create_alert(db=db)

    create = client_valid_access_token.post(
        "/api/analysis/", json={"node_tree": {"root_node_uuid": str(alert.uuid)}, key: value}
    )
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
def test_create_valid_optional_fields(client_valid_access_token, db, key, value):
    alert = helpers.create_alert(db=db)

    # Create the object
    create = client_valid_access_token.post(
        "/api/analysis/", json={"node_tree": {"root_node_uuid": str(alert.uuid)}, key: value}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details" and value:
        assert get.json()[key] == json.loads(value)
    else:
        assert get.json()[key] == value


def test_create_valid_analysis_module_type(client_valid_access_token, db):
    alert = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Use the analysis module type to create a new analysis
    create = client_valid_access_token.post(
        "/api/analysis/",
        json={"node_tree": {"root_node_uuid": str(alert.uuid)}, "analysis_module_type": str(analysis_module_type.uuid)},
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["analysis_module_type"]["uuid"] == str(analysis_module_type.uuid)


def test_create_valid_required_fields(client_valid_access_token, db):
    alert = helpers.create_alert(db=db)

    # Create the object
    create = client_valid_access_token.post("/api/analysis/", json={"node_tree": {"root_node_uuid": str(alert.uuid)}})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back, but since there are no required fields to create the analysis, there is nothing to verify.
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == 200


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_create_valid_node_directives(client_valid_access_token, db, values):
    alert = helpers.create_alert(db=db)
    for value in values:
        helpers.create_node_directive(value=value, db=db)

    # Create the node
    create = client_valid_access_token.post(
        "/api/analysis/", json={"node_tree": {"root_node_uuid": str(alert.uuid)}, "directives": values}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["directives"]) == len(list(set(values)))


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_create_valid_node_tags(client_valid_access_token, db, values):
    alert = helpers.create_alert(db=db)
    for value in values:
        helpers.create_node_tag(value=value, db=db)

    # Create the node
    create = client_valid_access_token.post(
        "/api/analysis/", json={"node_tree": {"root_node_uuid": str(alert.uuid)}, "tags": values}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["tags"]) == len(list(set(values)))


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_create_valid_node_threat_actor(client_valid_access_token, db, value):
    alert = helpers.create_alert(db=db)
    if value:
        helpers.create_node_threat_actor(value=value, db=db)

    # Create the node
    create = client_valid_access_token.post(
        "/api/analysis/", json={"node_tree": {"root_node_uuid": str(alert.uuid)}, "threat_actor": value}
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
def test_create_valid_node_threats(client_valid_access_token, db, values):
    alert = helpers.create_alert(db=db)
    for value in values:
        helpers.create_node_threat(value=value, types=["test_type"], db=db)

    # Create the node
    create = client_valid_access_token.post(
        "/api/analysis/", json={"node_tree": {"root_node_uuid": str(alert.uuid)}, "threats": values}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(set(values))
