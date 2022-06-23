import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/submission/comment/1?history_username=analyst")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/submission/comment/{uuid.uuid4()}?history_username=analyst")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete_submissions(client, db):
    # Create a comment
    submission = factory.submission.create(db=db, history_username="analyst")
    comment = factory.submission_comment.create_or_read(submission=submission, username="analyst", value="test", db=db)
    assert submission.comments[0].value == "test"

    # Delete it
    delete = client.delete(f"/api/submission/comment/{comment.uuid}?history_username=analyst")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/submission/comment/{comment.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # And make sure the submission no longer shows the comment
    assert len(submission.comments) == 0

    # Verify the history record
    history = client.get(f"/api/submission/{submission.uuid}/history")
    assert history.json()["total"] == 3
    assert history.json()["items"][2]["action"] == "UPDATE"
    assert history.json()["items"][2]["action_by"]["username"] == "analyst"
    assert history.json()["items"][2]["record_uuid"] == str(submission.uuid)
    assert history.json()["items"][2]["field"] == "comments"
    assert history.json()["items"][2]["diff"]["old_value"] is None
    assert history.json()["items"][2]["diff"]["new_value"] is None
    assert history.json()["items"][2]["diff"]["added_to_list"] == []
    assert history.json()["items"][2]["diff"]["removed_from_list"] == ["test"]
    assert history.json()["items"][2]["snapshot"]["comments"] == []
