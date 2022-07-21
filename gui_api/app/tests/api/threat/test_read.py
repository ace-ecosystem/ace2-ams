from urllib.parse import unquote_plus, urlencode
from uuid import uuid4


def test_get_all_threats(client_valid_access_token, requests_mock):
    params = urlencode({"limit": 50, "offset": 0})

    requests_mock.get(f"http://db-api/api/threat/?{params}", json={"items": [], "total": 0, "limit": 50, "offset": 0})

    client_valid_access_token.get(f"/api/threat/?{params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert unquote_plus(requests_mock.request_history[1].url) == unquote_plus(f"http://db-api/api/threat/?{params}")


def test_get_threat(client_valid_access_token, requests_mock):
    threat_uuid = uuid4()
    requests_mock.get(
        f"http://db-api/api/threat/{threat_uuid}",
        json={
            "types": [],
            "value": "value",
            "queues": [],
            "uuid": str(uuid4()),
        },
    )

    client_valid_access_token.get(f"/api/threat/{threat_uuid}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/threat/{threat_uuid}"
