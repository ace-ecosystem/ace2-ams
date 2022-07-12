import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/analysis/summary_detail/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/analysis/summary_detail/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client, db):
    submission = factory.submission.create(db=db)
    factory.format.create_or_read(value="PRE", db=db)

    # Create the object
    obj = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", format="PRE", db=db
    )
    assert len(submission.root_analysis.summary_details) == 1

    # Delete it
    delete = client.delete(f"/api/analysis/summary_detail/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT
    assert len(submission.root_analysis.summary_details) == 0
