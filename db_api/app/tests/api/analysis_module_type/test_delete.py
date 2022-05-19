import uuid

from fastapi import status

from tests import factory


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/analysis/module_type/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/analysis/module_type/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client, db):
    # Create an analysis module type
    analysis_module_type = factory.analysis_module_type.create_or_read(
        value="test",
        observable_types=["test_type"],
        required_directives=["test_directive"],
        required_tags=["test_tag"],
        db=db,
    )

    # Read it back
    get = client.get(f"/api/analysis/module_type/{analysis_module_type.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client.delete(f"/api/analysis/module_type/{analysis_module_type.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/analysis/module_type/{analysis_module_type.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the node directive is still there
    get = client.get(f"/api/node/directive/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 1

    # Make sure the node tag is still there
    get = client.get(f"/api/node/tag/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 1

    # Make sure the observable type is still there
    get = client.get(f"/api/observable/type/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 1
