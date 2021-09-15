import uuid

from fastapi import status


#
# INVALID TESTS
#


def test_get_invalid_uuid(client_valid_token):
    get = client_valid_token.get("/api/analysis/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client_valid_token):
    get = client_valid_token.get(f"/api/analysis/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


# There is currently no get_all endpoint for analysis
# def test_get_all(client_valid_token):
#     # Create some objects
#     client_valid_token.post("/api/analysis/", json={})
#     client_valid_token.post("/api/analysis/", json={})

#     # Read them back
#     get = client_valid_token.get("/api/analysis/")
#     assert get.status_code == status.HTTP_200_OK
#     assert len(get.json()) == 2


# def test_get_all_empty(client_valid_token):
#     get = client_valid_token.get("/api/analysis/module_type/")
#     assert get.status_code == status.HTTP_200_OK
#     assert get.json() == []
