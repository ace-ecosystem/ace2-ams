from uuid import uuid4


def test_update_node_threat(client_valid_access_token, requests_mock):
    node_threat_uuid = str(uuid4())

    requests_mock.patch("http://db-api/api/node/threat/")

    client_valid_access_token.patch(f"/api/node/threat/{node_threat_uuid}", json={})

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "PATCH"
    assert requests_mock.request_history[1].url == f"http://db-api/api/node/threat/{node_threat_uuid}"
