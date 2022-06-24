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
        ("value", None),
        ("value", 123),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/submission/comment/{uuid.uuid4()}", json={key: value, "username": "analyst"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client):
    update = client.patch("/api/submission/comment/1", json={"value": "test", "username": "analyst"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_submission_uuid_value(client, db):
    submission = factory.submission.create(db=db)

    # Create some comments
    comment1 = factory.submission_comment.create_or_read(submission=submission, username="johndoe", value="test", db=db)
    comment2 = factory.submission_comment.create_or_read(
        submission=submission, username="johndoe", value="test2", db=db
    )

    # Make sure you cannot update a comment on a submission to one that already exists
    update = client.patch(
        f"/api/submission/comment/{comment2.uuid}", json={"value": comment1.value, "username": "johndoe"}
    )
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/submission/comment/{uuid.uuid4()}", json={"value": "test", "username": "analyst"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_submissions(client, db):
    # Create a comment
    submission = factory.submission.create(db=db, history_username="analyst")
    comment = factory.submission_comment.create_or_read(submission=submission, username="johndoe", value="test", db=db)
    original_time = comment.insert_time
    assert submission.comments[0].value == "test"
    assert comment.user.username == "johndoe"

    # Update it
    update = client.patch(f"/api/submission/comment/{comment.uuid}", json={"value": "updated", "username": "analyst"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert submission.comments[0].value == "updated"
    assert submission.comments[0].user.username == "analyst"
    assert submission.comments[0].insert_time != original_time

    # Verify the history record
    history = client.get(f"/api/submission/{submission.uuid}/history")

    assert history.json()["total"] == 3
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "johndoe"
    assert history.json()["items"][1]["record_uuid"] == str(submission.uuid)
    assert history.json()["items"][1]["field"] == "comments"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"

    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(submission.uuid)
    assert history.json()["items"][2]["field"] == "comments"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == ["updated"]
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["name"] == "Test Alert"
