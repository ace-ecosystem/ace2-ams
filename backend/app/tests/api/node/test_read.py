import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_version_invalid_uuid(client_valid_access_token):
    get = client_valid_access_token.get("/api/node/1/version")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_version_nonexistent_uuid(client_valid_access_token):
    get = client_valid_access_token.get(f"/api/node/{uuid.uuid4()}/version")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_version(client_valid_access_token, db):
    # Create a Node
    analysis = helpers.create_analysis(db=db)

    get = client_valid_access_token.get(f"/api/node/{analysis.uuid}/version")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {"version": str(analysis.version)}
