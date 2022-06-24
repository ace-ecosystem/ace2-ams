from uuid import uuid4


def test_update_threat(client_valid_access_token, requests_mock):
    threat_uuid = str(uuid4())

    requests_mock.patch(f"http://db-api/api/threat/{threat_uuid}")

    client_valid_access_token.patch(f"/api/threat/{threat_uuid}", json={})

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "PATCH"
    assert requests_mock.request_history[1].url == f"http://db-api/api/threat/{threat_uuid}"
