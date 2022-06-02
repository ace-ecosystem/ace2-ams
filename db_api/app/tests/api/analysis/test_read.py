import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/analysis/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/analysis/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get(client, db):
    submission = factory.submission.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test_type", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=submission.root_analysis, db=db
    )
    analysis = factory.analysis.create_or_read(
        analysis_module_type=analysis_module_type, submission=submission, target=observable, db=db
    )

    get = client.get(f"/api/analysis/{analysis.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["node_type"] == "analysis"
