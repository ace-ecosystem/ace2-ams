import pytest

from datetime import datetime
from urllib.parse import unquote_plus, urlencode
from uuid import uuid4


@pytest.mark.parametrize(
    "param,value",
    [
        ("alert_time_after", datetime.now()),
        ("alert_time_before", datetime.now()),
        ("contain_time_after", datetime.now()),
        ("contain_time_before", datetime.now()),
        ("created_time_after", datetime.now()),
        ("created_time_before", datetime.now()),
        ("disposition", "FALSE_POSITIVE"),
        ("disposition_time_after", datetime.now()),
        ("disposition_time_before", datetime.now()),
        ("event_type", "test_type"),
        ("name", "test"),
        ("observable", "fqdn|test.com"),
        ("observable_types", "fqdn,ipv4"),
        ("observable_value", "test.com"),
        ("owner", "analyst"),
        ("prevention_tools", "tool1,tool2"),
        ("queue", "test_queue"),
        ("remediation_time_after", datetime.now()),
        ("remediation_time_before", datetime.now()),
        ("remediations", "rem1,rem2"),
        ("risk_level", "test_level"),
        ("sort", "name|desc"),
        ("source", "test_source"),
        ("status", "OPEN"),
        ("tags", "tag1,tag2"),
        ("threat_actors", "actor1,actor2"),
        ("threats", "threat1,threat2"),
        ("vectors", "vector1,vector2"),
    ],
)
def test_get_all_events(client_valid_access_token, requests_mock, param, value):
    params = urlencode({"limit": 50, "offset": 0, param: value})

    requests_mock.get(f"http://db-api/api/event/?{params}", json={"items": [], "total": 0, "limit": 50, "offset": 0})

    client_valid_access_token.get(f"/api/event/?{params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert unquote_plus(requests_mock.request_history[1].url) == unquote_plus(f"http://db-api/api/event/?{params}")


def test_get_event(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    requests_mock.get(f"http://db-api/api/event/{event_uuid}", json={})

    client_valid_access_token.get(f"/api/event/{event_uuid}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}"


def test_get_event_history(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    params = urlencode({"limit": 50, "offset": 0})
    requests_mock.get(
        f"http://db-api/api/event/{event_uuid}/history?{params}",
        json={"items": [], "total": 0, "limit": 50, "offset": 0},
    )

    client_valid_access_token.get(f"/api/event/{event_uuid}/history?{params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}/history?{params}"


#
# SUMMARIES
#


def test_get_detection_point_summary(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    requests_mock.get(f"http://db-api/api/event/{event_uuid}/summary/detection_point", json=[])

    client_valid_access_token.get(f"/api/event/{event_uuid}/summary/detection_point")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}/summary/detection_point"


def test_get_email_headers_body_summary(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    requests_mock.get(
        f"http://db-api/api/event/{event_uuid}/summary/email_headers_body",
        json={"headers": "asdf", "alert_uuid": str(uuid4())},
    )

    client_valid_access_token.get(f"/api/event/{event_uuid}/summary/email_headers_body")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}/summary/email_headers_body"


def test_get_email_summary(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    requests_mock.get(f"http://db-api/api/event/{event_uuid}/summary/email", json=[])

    client_valid_access_token.get(f"/api/event/{event_uuid}/summary/email")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}/summary/email"


def test_get_observable_summary(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    requests_mock.get(f"http://db-api/api/event/{event_uuid}/summary/observable", json=[])

    client_valid_access_token.get(f"/api/event/{event_uuid}/summary/observable")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}/summary/observable"


def test_get_sandbox_summary(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    requests_mock.get(f"http://db-api/api/event/{event_uuid}/summary/sandbox", json=[])

    client_valid_access_token.get(f"/api/event/{event_uuid}/summary/sandbox")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}/summary/sandbox"


def test_get_user_summary(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    requests_mock.get(f"http://db-api/api/event/{event_uuid}/summary/user", json=[])

    client_valid_access_token.get(f"/api/event/{event_uuid}/summary/user")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}/summary/user"


def test_get_url_domain_summary(client_valid_access_token, requests_mock):
    event_uuid = uuid4()
    requests_mock.get(
        f"http://db-api/api/event/{event_uuid}/summary/url_domain",
        json={"domains": [], "total": 0},
    )

    client_valid_access_token.get(f"/api/event/{event_uuid}/summary/url_domain")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/event/{event_uuid}/summary/url_domain"
