from fastapi import status


def test_unexpected_status_code(client_valid_access_token, requests_mock):
    requests_mock.get(f"http://db-api/api/user/", status_code=status.HTTP_418_IM_A_TEAPOT)

    result = client_valid_access_token.get(f"/api/user/")
    assert result.status_code == status.HTTP_418_IM_A_TEAPOT
