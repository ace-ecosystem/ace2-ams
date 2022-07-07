import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/metadata/sort/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/metadata/sort/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client, db):
    # Create some objects
    factory.metadata_sort.create_or_read(value=1, db=db)
    factory.metadata_sort.create_or_read(value=2, db=db)

    # Read them back
    get = client.get("/api/metadata/sort/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 2


def test_get_all_empty(client):
    get = client.get("/api/metadata/sort/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 0
