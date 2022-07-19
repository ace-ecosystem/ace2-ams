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
        ("content", 123),
        ("content", None),
        ("content", ""),
        ("format", 123),
        ("format", None),
        ("format", ""),
        ("header", 123),
        ("header", None),
        ("header", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/analysis/summary_detail/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client):
    update = client.patch("/api/analysis/summary_detail/1", json={"content": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_unique_fields(client, db):
    submission = factory.submission.create(db=db)

    # Create some objects
    obj1 = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test1", content="test1", db=db
    )
    obj2 = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test2", content="test2", db=db
    )

    # Ensure you cannot update a unique field to a value that already exists
    update = client.patch(f"/api/analysis/summary_detail/{obj2.uuid}", json={"header": "test1", "content": "test1"})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_format(client, db):
    submission = factory.submission.create(db=db)

    obj = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test1", content="test1", format="PRE", db=db
    )

    update = client.patch(f"/api/analysis/summary_detail/{obj.uuid}", json={"format": "TEXT"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/analysis/summary_detail/{uuid.uuid4()}", json={"content": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("content", "test", "test2"),
        ("content", "test", "test"),
        ("header", "test", "test2"),
        ("header", "test", "test"),
    ],
)
def test_update(client, db, key, initial_value, updated_value):
    submission = factory.submission.create(db=db)

    # Create the object
    obj = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", db=db
    )

    # Set the initial value
    setattr(obj, key, initial_value)

    # Update it
    update = client.patch(f"/api/analysis/summary_detail/{obj.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert getattr(obj, key) == updated_value


def test_update_format(client, db):
    submission = factory.submission.create(db=db)
    factory.format.create_or_read(value="PRE", db=db)
    factory.format.create_or_read(value="TEXT", db=db)

    # Create the object
    obj = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", format="PRE", db=db
    )
    assert obj.format.value == "PRE"

    # Update it
    update = client.patch(f"/api/analysis/summary_detail/{obj.uuid}", json={"format": "TEXT"})
    print(update.text)
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert obj.format.value == "TEXT"
