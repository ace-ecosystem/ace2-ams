from fastapi import status

from tests.helpers import create_test_user


#
# VALID TESTS
#


def test_auth_logout_success(client, db):
    create_test_user(db, "johndoe", "abcd1234")

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "johndoe", "password": "abcd1234"})
    access_token = auth.json()["access_token"]
    refresh_token = auth.json()["refresh_token"]
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["token_type"] == "bearer"
    assert access_token
    assert refresh_token
    # Because the cookie values have a space in them, the entire string is quoted.
    assert auth.cookies["access_token"] == f'"Bearer {access_token}"'
    assert auth.cookies["refresh_token"] == f'"Bearer {refresh_token}"'

    # Attempt to use the access token to logout
    logout = client.get("/api/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert logout.status_code == status.HTTP_200_OK
    assert logout.json() is None
    assert "access_token" not in logout.cookies
    assert "refresh_token" not in logout.cookies
