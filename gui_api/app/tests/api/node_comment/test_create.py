from uuid import uuid4


def test_create_node_comment(client_valid_access_token, requests_mock):
    requests_mock.post("http://db-api/api/node/comment/?history_username=analyst", json=[{"uuid": "uuid1"}])

    client_valid_access_token.post(
        "/api/node/comment/",
        json=[{"node_uuid": str(uuid4()), "value": "value", "username": "analyst"}],
    )

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == "http://db-api/api/node/comment/?history_username=analyst"
