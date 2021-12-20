import json
import pytest
import uuid

from fastapi import status

from tests.api.node import (
    INVALID_UPDATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTORS,
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
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/analysis/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(update.json()["detail"]) == 1
    assert key in update.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key,value",
    INVALID_UPDATE_FIELDS,
)
def test_update_invalid_node_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/analysis/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(update.json()["detail"]) == 1
    assert key in update.json()["detail"][0]["loc"]


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/analysis/1", json={})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token, db):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client_valid_access_token.patch(f"/api/analysis/{analysis.uuid}", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_analysis_module_type(client_valid_access_token, db):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)

    # Make sure you cannot update it to use a nonexistent analysis module type
    update = client_valid_access_token.patch(
        f"/api/analysis/{analysis.uuid}",
        json={"analysis_module_type": str(uuid.uuid4())},
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_update_nonexistent_node_fields(client_valid_access_token, db, key, value):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch(f"/api/analysis/{analysis.uuid}", json={key: value})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/analysis/{uuid.uuid4()}", json={})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_analysis_module_type(client_valid_access_token, db):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)
    initial_analysis_version = analysis.version

    # Create a new analysis module type
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Update the analysis module type
    update = client_valid_access_token.patch(
        f"/api/analysis/{analysis.uuid}",
        json={"analysis_module_type": str(analysis_module_type.uuid)},
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert analysis.analysis_module_type == analysis_module_type
    assert analysis.version != initial_analysis_version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_update_valid_node_directives(client_valid_access_token, db, values):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)
    initial_analysis_version = analysis.version

    # Create the directives
    for value in values:
        helpers.create_node_directive(value=value, db=db)

    # Update the analysis
    update = client_valid_access_token.patch(f"/api/analysis/{analysis.uuid}", json={"directives": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(analysis.directives) == len(set(values))
    assert analysis.version != initial_analysis_version


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_update_valid_node_tags(client_valid_access_token, db, values):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)
    initial_analysis_version = analysis.version

    # Create the tags
    for value in values:
        helpers.create_node_tag(value=value, db=db)

    # Update the node
    update = client_valid_access_token.patch(f"/api/analysis/{analysis.uuid}", json={"tags": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(analysis.tags) == len(set(values))
    assert analysis.version != initial_analysis_version


@pytest.mark.parametrize(
    "values",
    VALID_THREAT_ACTORS,
)
def test_update_valid_node_threat_actors(client_valid_access_token, db, values):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)
    initial_analysis_version = analysis.version

    # Create the threat actor
    for value in values:
        helpers.create_node_threat_actor(value=value, db=db)

    # Update the node
    update = client_valid_access_token.patch(f"/api/analysis/{analysis.uuid}", json={"threat_actors": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(analysis.threat_actors) == len(set(values))
    assert analysis.version != initial_analysis_version


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_update_valid_node_threats(client_valid_access_token, db, values):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)
    initial_analysis_version = analysis.version

    # Create the threats
    for value in values:
        helpers.create_node_threat(value=value, types=["test_type"], db=db)

    # Update the node
    update = client_valid_access_token.patch(f"/api/analysis/{analysis.uuid}", json={"threats": values})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert len(analysis.threats) == len(set(values))
    assert analysis.version != initial_analysis_version


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("details", None, '{"foo": "bar"}'),
        ("details", '{"foo": "bar"}', '{"foo": "bar"}'),
        ("error_message", None, "test"),
        ("error_message", "test", "test"),
        ("stack_trace", None, "test"),
        ("stack_trace", "test", "test"),
        ("summary", None, "test"),
        ("summary", "test", "test"),
    ],
)
def test_update(client_valid_access_token, db, key, initial_value, updated_value):
    # Create an analysis
    analysis = helpers.create_analysis(db=db)
    initial_analysis_version = analysis.version

    # Set the initial value
    setattr(analysis, key, initial_value)

    # Update it
    update = client_valid_access_token.patch(f"/api/analysis/{analysis.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if key == "details":
        assert analysis.details == json.loads(updated_value)
    else:
        assert getattr(analysis, key) == updated_value

    assert analysis.version != initial_analysis_version
