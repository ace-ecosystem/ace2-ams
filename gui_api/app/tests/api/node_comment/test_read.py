from datetime import datetime
from uuid import uuid4


def test_get_node_comment(client_valid_access_token, requests_mock):
    node_comment_uuid = uuid4()
    requests_mock.get(
        f"http://db-api/api/node/comment/{node_comment_uuid}",
        json={
            "node_uuid": str(uuid4()),
            "value": "value",
            "insert_time": str(datetime.now()),
            "user": {
                "default_alert_queue": {"value": "queue1", "uuid": str(uuid4())},
                "default_event_queue": {"value": "queue1", "uuid": str(uuid4())},
                "display_name": "Analyst",
                "email": "analyst@test.com",
                "roles": [],
                "username": "analyst",
                "uuid": str(uuid4()),
            },
            "uuid": str(uuid4()),
        },
    )

    client_valid_access_token.get(f"/api/node/comment/{node_comment_uuid}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/node/comment/{node_comment_uuid}"
