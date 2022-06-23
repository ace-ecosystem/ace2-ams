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
        ("submission_uuid", 123),
        ("submission_uuid", None),
        ("submission_uuid", ""),
        ("submission_uuid", "abc"),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client, key, value):
    create = client.post("/api/submission/comment/", json=[{key: value, "username": "analyst"}])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_submission_uuid(client):
    # Create a comment
    create_json = {
        "submission_uuid": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "value": "test",
        "username": "analyst",
    }
    create = client.post("/api/submission/comment/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_create_verify_history_submissions(client, db):
    submission = factory.submission.create(db=db, history_username="analyst")

    # Add a comment to the submission
    create_json = [
        {"submission_uuid": str(submission.uuid), "value": "test", "username": "analyst"},
    ]
    create = client.post("/api/submission/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(submission.uuid)
    assert history.json()["items"][1]["field"] == "comments"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"


def test_create_multiple(client, db):
    submission1 = factory.submission.create(db=db)
    initial_submission1_version = submission1.version

    submission2 = factory.submission.create(db=db)
    initial_submission2_version = submission2.version

    submission3 = factory.submission.create(db=db)
    initial_submission3_version = submission3.version

    assert submission1.comments == []
    assert submission2.comments == []
    assert submission3.comments == []

    # Add a comment to each submission at once
    create_json = [
        {"submission_uuid": str(submission1.uuid), "value": "test1", "username": "analyst"},
        {"submission_uuid": str(submission2.uuid), "value": "test2", "username": "analyst"},
        {"submission_uuid": str(submission3.uuid), "value": "test3", "username": "analyst"},
    ]
    create = client.post("/api/submission/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    assert len(submission1.comments) == 1
    assert submission1.comments[0].value == "test1"
    assert submission1.comments[0].user.username == "analyst"
    assert submission1.version != initial_submission1_version

    assert len(submission2.comments) == 1
    assert submission2.comments[0].value == "test2"
    assert submission2.comments[0].user.username == "analyst"
    assert submission2.version != initial_submission2_version

    assert len(submission3.comments) == 1
    assert submission3.comments[0].value == "test3"
    assert submission3.comments[0].user.username == "analyst"
    assert submission3.version != initial_submission3_version


def test_create_valid_required_fields(client, db):
    submission = factory.submission.create(db=db)
    initial_submission_version = submission.version

    # Create a comment
    create_json = {
        "submission_uuid": str(submission.uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test",
        "username": "analyst",
    }
    create = client.post("/api/submission/comment/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED
    assert len(submission.comments) == 1
    assert submission.comments[0].value == "test"
    assert submission.comments[0].user.username == "analyst"
    assert submission.version != initial_submission_version
