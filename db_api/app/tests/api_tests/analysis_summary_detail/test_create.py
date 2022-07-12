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
        ("analysis_uuid", None),
        ("analysis_uuid", 1),
        ("analysis_uuid", "abc"),
        ("analysis_uuid", ""),
        ("content", 123),
        ("content", None),
        ("content", ""),
        ("format", 123),
        ("format", None),
        ("format", ""),
        ("header", 123),
        ("header", None),
        ("header", ""),
        ("uuid", None),
        ("uuid", 1),
        ("uuid", "abc"),
        ("uuid", ""),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = [
        {
            "analysis_uuid": str(uuid.uuid4()),
            "content": "test",
            "format": "PRE",
            "header": "test",
            key: value,
        }
    ]
    create = client.post("/api/analysis/summary_detail/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("analysis_uuid"),
        ("content"),
        ("format"),
        ("header"),
    ],
)
def test_create_missing_required_fields(client, key):
    create_json = [{"analysis_uuid": str(uuid.uuid4()), "content": "test", "format": "PRE", "header": "test"}]
    del create_json[0][key]
    create = client.post("/api/analysis/summary_detail/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_analysis_uuid(client, db):
    factory.format.create_or_read(value="PRE", db=db)

    create_json = [{"analysis_uuid": str(uuid.uuid4()), "content": "test", "format": "PRE", "header": "test"}]
    create = client.post("/api/analysis/summary_detail/", json=create_json)
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_nonexistent_format(client, db):
    submission = factory.submission.create(db=db)

    create_json = [
        {"analysis_uuid": str(submission.root_analysis_uuid), "content": "test", "format": "PRE", "header": "test"}
    ]
    create = client.post("/api/analysis/summary_detail/", json=create_json)
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client, db, key, value):
    submission = factory.submission.create(db=db)
    factory.format.create_or_read(value="PRE", db=db)

    # Create the object
    create = client.post(
        "/api/analysis/summary_detail/",
        json=[
            {
                "analysis_uuid": str(submission.root_analysis_uuid),
                "content": "test",
                "format": "PRE",
                "header": "test",
                key: value,
            }
        ],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client, db):
    submission = factory.submission.create(db=db)
    factory.format.create_or_read(value="PRE", db=db)

    # Create the object
    create = client.post(
        "/api/analysis/summary_detail/",
        json=[
            {"analysis_uuid": str(submission.root_analysis_uuid), "content": "test", "format": "PRE", "header": "test"}
        ],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["content"] == "test"
