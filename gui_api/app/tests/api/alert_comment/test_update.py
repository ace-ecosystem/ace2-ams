from fastapi import status
from uuid import uuid4


def test_update_alert_comment(client_valid_access_token, requests_mock):
    alert_comment_uuid = str(uuid4())

    requests_mock.patch(
        f"http://db-api/api/submission/comment/{alert_comment_uuid}",
        status_code=status.HTTP_204_NO_CONTENT,
    )

    client_valid_access_token.patch(
        f"/api/alert/comment/{alert_comment_uuid}", json={"username": "analyst", "value": "value"}
    )

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "PATCH"
    assert requests_mock.request_history[1].url == f"http://db-api/api/submission/comment/{alert_comment_uuid}"
