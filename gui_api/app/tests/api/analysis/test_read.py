from uuid import uuid4


def test_get_analysis(client_valid_access_token, requests_mock):
    analysis_uuid = str(uuid4())
    requests_mock.get(
        f"http://db-api/api/analysis/{analysis_uuid}",
        json={"node_type": "analysis", "uuid": analysis_uuid, "detection_points": []},
    )

    client_valid_access_token.get(f"/api/analysis/{analysis_uuid}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/analysis/{analysis_uuid}"
