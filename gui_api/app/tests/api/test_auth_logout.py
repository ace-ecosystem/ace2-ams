from fastapi import status
from uuid import uuid4


def test_auth_logout(client, requests_mock):
    requests_mock.post(
        "http://db-api/api/auth",
        json={
            "default_alert_queue": {"value": "queue1", "uuid": str(uuid4())},
            "default_event_queue": {"value": "queue1", "uuid": str(uuid4())},
            "display_name": "Analyst",
            "email": "analyst@test.com",
            "roles": [],
            "username": "analyst",
            "uuid": str(uuid4()),
        },
    )

    # Attempt to authenticate
    auth = client.post("/api/auth", data={"username": "analyst", "password": "asdfasdf"})
    assert auth.status_code == status.HTTP_200_OK
    assert auth.json()["username"] == "analyst"
    assert auth.cookies.get("access_token")
    assert auth.cookies.get("refresh_token")

    # Attempt to use the token to access a protected API endpoint
    get = client.get("/api/user/", cookies=auth.cookies)
    assert get.status_code == status.HTTP_200_OK

    # Attempt to use the access token to logout
    logout = client.get("/api/auth/logout", cookies=auth.cookies)
    assert logout.status_code == status.HTTP_200_OK
    assert logout.json() is None
    assert "access_token" not in logout.cookies
    assert "refresh_token" not in logout.cookies
