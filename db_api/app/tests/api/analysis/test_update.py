import json
import pytest
import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
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
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/analysis/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(update.json()["detail"]) == 1
    assert key in update.json()["detail"][0]["loc"]


def test_update_invalid_uuid(client):
    update = client.patch("/api/analysis/1", json={})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client, db):
    alert_tree = helpers.create_alert(db=db)
    analysis_tree = helpers.create_analysis(parent_tree=alert_tree, db=db)

    # Make sure you cannot update it using an invalid version. The version is
    # optional, but if given, it must match.
    update = client.patch(
        f"/api/analysis/{analysis_tree.node.uuid}", json={"version": str(uuid.uuid4())}
    )
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/analysis/{uuid.uuid4()}", json={})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("details", None, '{"foo": "bar"}'),
        ("details", '{"foo": "bar"}', None),
        ("details", '{"foo": "bar"}', '{"foo": "bar"}'),
        ("error_message", None, "test"),
        ("error_message", "test", None),
        ("error_message", "test", "test"),
        ("stack_trace", None, "test"),
        ("stack_trace", "test", None),
        ("stack_trace", "test", "test"),
        ("summary", None, "test"),
        ("summary", "test", None),
        ("summary", "test", "test"),
    ],
)
def test_update(client, db, key, initial_value, updated_value):
    alert_tree = helpers.create_alert(db=db)
    analysis_tree = helpers.create_analysis(parent_tree=alert_tree, db=db)
    initial_analysis_version = analysis_tree.node.version

    # Set the initial value
    setattr(analysis_tree.node, key, initial_value)

    # Update it
    update = client.patch(f"/api/analysis/{analysis_tree.node.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if key == "details" and updated_value:
        assert analysis_tree.node.details == json.loads(updated_value)
    else:
        assert getattr(analysis_tree.node, key) == updated_value

    assert analysis_tree.node.version != initial_analysis_version
