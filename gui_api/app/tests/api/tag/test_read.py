from urllib.parse import unquote_plus, urlencode
from uuid import uuid4


def test_get_all_tags(client_valid_access_token, requests_mock):
    params = urlencode({"limit": 50, "offset": 0})

    requests_mock.get(f"http://db-api/api/tag/?{params}", json={"items": [], "total": 0, "limit": 50, "offset": 0})

    client_valid_access_token.get(f"/api/tag/?{params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert unquote_plus(requests_mock.request_history[1].url) == unquote_plus(f"http://db-api/api/tag/?{params}")


def test_get_tag(client_valid_access_token, requests_mock):
    tag_uuid = uuid4()
    requests_mock.get(
        f"http://db-api/api/tag/{tag_uuid}", json={"metadata_type": "tag", "value": "value", "uuid": str(uuid4())}
    )

    client_valid_access_token.get(f"/api/tag/{tag_uuid}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/tag/{tag_uuid}"
