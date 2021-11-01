import uuid

from fastapi import status

from tests import helpers


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete("/api/analysis/module_type/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete(f"/api/analysis/module_type/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client_valid_access_token, db):
    # Create an analysis module type
    analysis_module_type = helpers.create_analysis_module_type(
        value="test",
        observable_types=["test_type"],
        required_directives=["test_directive"],
        required_tags=["test_tag"],
        db=db,
    )
    directive_uuid = analysis_module_type.required_directives[0].uuid
    observable_type_uuid = analysis_module_type.observable_types[0].uuid
    tag_uuid = analysis_module_type.required_tags[0].uuid

    # Read it back
    get = client_valid_access_token.get(f"/api/analysis/module_type/{analysis_module_type.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client_valid_access_token.delete(f"/api/analysis/module_type/{analysis_module_type.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(f"/api/analysis/module_type/{analysis_module_type.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the node directive is still there
    get = client_valid_access_token.get(f"/api/node/directive/{directive_uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_directive"

    # Make sure the node tag is still there
    get = client_valid_access_token.get(f"/api/node/tag/{tag_uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_tag"

    # Make sure the observable type is still there
    get = client_valid_access_token.get(f"/api/observable/type/{observable_type_uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_type"
