import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/analysis/summary_detail/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/analysis/summary_detail/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get(client, db):
    submission = factory.submission.create(db=db)
    summary_detail = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", db=db
    )

    get = client.get(f"/api/analysis/summary_detail/{summary_detail.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["uuid"] == str(summary_detail.uuid)
