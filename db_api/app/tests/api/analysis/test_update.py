import json
import pytest
import uuid

from fastapi import status

from tests import factory


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
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test_type", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )
    analysis = factory.analysis.create_or_read(
        analysis_module_type=analysis_module_type, submission=alert, target=observable, db=db
    )

    # Set the initial value
    setattr(analysis, key, initial_value)

    # Update it
    update = client.patch(f"/api/analysis/{analysis.uuid}", json={key: updated_value})
    print(update.text)
    assert update.status_code == status.HTTP_204_NO_CONTENT

    if key == "details" and updated_value:
        assert analysis.details == json.loads(updated_value)
    else:
        assert getattr(analysis, key) == updated_value
