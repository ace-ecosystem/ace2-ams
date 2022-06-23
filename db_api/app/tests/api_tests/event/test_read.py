import json
import pytest
import uuid

from datetime import datetime, timedelta
from dateutil.parser import parse
from fastapi import status
from urllib.parse import urlencode

from api_models.analysis_details import (
    SandboxAnalysisDetails,
    SandboxContactedHost,
    SandboxDnsRequest,
    SandboxDroppedFile,
    SandboxHttpRequest,
    SandboxProcess,
)
from tests import factory


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/event/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/event/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "path",
    [
        ("/summary/detection_point"),
        ("/summary/email_headers_body"),
        ("/summary/email"),
        ("/summary/observable"),
        ("/summary/sandbox"),
        ("/summary/user"),
        ("/summary/url_domain"),
    ],
)
def test_get_summary_nonexistent_event(client, path):
    get = client.get(f"/api/event/{uuid.uuid4()}{path}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_summary_detection_point(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The detection point summary should be empty
    get = client.get(f"/api/event/{event.uuid}/summary/detection_point")
    assert get.json() == []

    # Add some alerts with detection points to the event
    #
    # alert1
    #   o1 - detection point 1, detection point 2
    #
    # alert2
    #   o1 - detection point 2, detection point 3
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="test_type",
        value="test_value",
        parent_analysis=alert1.root_analysis,
        detection_points=["detection point 1", "detection point 2"],
        db=db,
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="test_type",
        value="test_value2",
        parent_analysis=alert2.root_analysis,
        detection_points=["detection point 2", "detection point 3"],
        db=db,
    )

    # The detection point summary should now have 3 entries (since one detection point was repeated).
    # They should be sorted by the detection point values
    get = client.get(f"/api/event/{event.uuid}/summary/detection_point")
    assert len(get.json()) == 3
    assert get.json()[0]["count"] == 1
    assert get.json()[0]["alert_uuid"] == str(alert1.uuid)
    assert get.json()[0]["value"] == "detection point 1"
    assert get.json()[1]["count"] == 2
    assert get.json()[1]["alert_uuid"]
    assert get.json()[1]["value"] == "detection point 2"
    assert get.json()[2]["count"] == 1
    assert get.json()[2]["alert_uuid"] == str(alert2.uuid)
    assert get.json()[2]["value"] == "detection point 3"


def test_summary_email(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The email summary should be empty
    get = client.get(f"/api/event/{event.uuid}/summary/email")
    assert get.json() == []

    # Add some alerts with analysis to the event
    #
    # alert1
    #   o1
    #     a1 - email analysis 1
    #
    # alert2
    #  o1
    #    a1 - email analysis 2
    #
    # alert3
    #  o1
    #    a1 - email analysis 2
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="file",
        value="6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        parent_analysis=alert1.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "blah",
            "message_id": "<abcd1234@evil.com>",
            "subject": "Hello",
            "time": datetime.now().isoformat(),
            "to_address": "goodguy@company.com",
        },
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="file",
        value="d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
        parent_analysis=alert2.root_analysis,
        db=db,
    )
    time = datetime.now().isoformat()
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert2,
        target=alert2_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "blah",
            "message_id": "<1234abcd@evil.com>",
            "subject": "Hello",
            "time": time,
            "to_address": "otherguy@company.com",
        },
    )

    # Add a third alert that has the exact same analysis as one of the others
    alert3 = factory.submission.create(db=db, event=event)
    alert3_o1 = factory.observable.create_or_read(
        type="file",
        value="d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
        parent_analysis=alert3.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert3,
        target=alert3_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "blah",
            "message_id": "<1234abcd@evil.com>",
            "subject": "Hello",
            "time": time,
            "to_address": "otherguy@company.com",
        },
    )

    # Add a fourth alert that is not part of the event
    alert4 = factory.submission.create(db=db)
    alert4_o1 = factory.observable.create_or_read(
        type="file",
        value="4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce",
        parent_analysis=alert4.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert4,
        target=alert4_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "neutralguy@okay.com",
            "headers": "blah",
            "message_id": "<1234abcd@okay.com>",
            "subject": "Hi",
            "time": datetime.now().isoformat(),
            "to_address": "goodguy@company.com",
        },
    )

    # The email summary should now have two entries in it. Even though one of the emails was repeated two
    # times across the alerts, its Email Analysis is going to be the same for each, so it appears once in the summary.
    # Additionally, the results should be sorted by the email time.
    get = client.get(f"/api/event/{event.uuid}/summary/email")
    assert len(get.json()) == 2
    assert get.json()[0]["message_id"] == "<abcd1234@evil.com>"
    assert get.json()[1]["message_id"] == "<1234abcd@evil.com>"


def test_summary_email_headers_body(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The email headers/body summary should be empty
    get = client.get(f"/api/event/{event.uuid}/summary/email_headers_body")
    assert get.json() is None

    # Add some alerts with analysis to the event
    #
    # alert1
    #   o1
    #     a1 - email analysis 1
    #
    # alert2
    #  o1
    #    a1 - email analysis 2
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="file",
        value="6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        parent_analysis=alert1.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
        details={
            "attachments": [],
            "body_html": "<p>body1</p>",
            "body_text": "body1",
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "headers1",
            "message_id": "<abcd1234@evil.com>",
            "subject": "Hello",
            "time": datetime.now().isoformat(),
            "to_address": "goodguy@company.com",
        },
    )

    # The second alert's email has an earlier time
    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="file",
        value="d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
        parent_analysis=alert2.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert2,
        target=alert2_o1,
        details={
            "attachments": [],
            "body_html": "<p>body2</p>",
            "body_text": "body2",
            "cc_addresses": [],
            "from_address": "badguy@evil.com",
            "headers": "headers2",
            "message_id": "<1234abcd@evil.com>",
            "subject": "Hello",
            "time": (datetime.now() - timedelta(days=1)).isoformat(),
            "to_address": "otherguy@company.com",
        },
    )

    # Add an alert that is not part of the event
    alert3 = factory.submission.create(db=db)
    alert3_o1 = factory.observable.create_or_read(
        type="file",
        value="4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce",
        parent_analysis=alert3.root_analysis,
        db=db,
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Email Analysis", db=db),
        submission=alert3,
        target=alert3_o1,
        details={
            "attachments": [],
            "cc_addresses": [],
            "from_address": "neutralguy@okay.com",
            "headers": "blah",
            "message_id": "<1234abcd@okay.com>",
            "subject": "Hi",
            "time": datetime.now().isoformat(),
            "to_address": "goodguy@company.com",
        },
    )

    # The email headers/body summary should now have the details of the second alert's email
    get = client.get(f"/api/event/{event.uuid}/summary/email_headers_body")
    assert get.json()["alert_uuid"] == str(alert2.uuid)
    assert get.json()["headers"] == "headers2"
    assert get.json()["body_html"] == "<p>body2</p>"
    assert get.json()["body_text"] == "body2"


def test_summary_observable(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The observable summary should be empty
    get = client.get(f"/api/event/{event.uuid}/summary/observable")
    assert get.json() == []

    # Add some alerts with analyses to the event
    #
    # alert1
    #   o1
    #     a1
    #       o2 - 127.0.0.1
    #         a2 - FA Q
    #   o3 - 127.0.0.1
    #     a3 - FA Q
    #
    # alert2
    #  o1 - 127.0.0.1
    #    a1 - FA Q
    #  o2 - 192.168.1.1
    #    a2 - FA Q
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="fqdn", value="localhost.localdomain", parent_analysis=alert1.root_analysis, db=db
    )
    alert1_a1 = factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FQDN Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
    )
    alert1_o2 = factory.observable.create_or_read(type="ipv4", value="127.0.0.1", parent_analysis=alert1_a1, db=db)
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 1", db=db),
        submission=alert1,
        target=alert1_o2,
        details={"link": "https://url.to.search/query=asdf", "hits": 10},
    )
    alert1_o3 = factory.observable.create_or_read(
        type="ipv4", value="127.0.0.1", parent_analysis=alert1.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 1", db=db),
        submission=alert1,
        target=alert1_o3,
        details={"link": "https://url.to.search/query=asdf", "hits": 10},
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="ipv4", value="127.0.0.1", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 1", db=db),
        submission=alert2,
        target=alert2_o1,
        details={"link": "https://url.to.search/query=asdf", "hits": 10},
    )
    alert2_o2 = factory.observable.create_or_read(
        type="ipv4", value="192.168.1.1", parent_analysis=alert2.root_analysis, db=db
    )
    # This FA Queue analysis doesn't have a "link" field
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 2", db=db),
        submission=alert2,
        target=alert2_o2,
        details={"hits": 100},
    )

    # Add a third alert that is not part of the event
    alert3 = factory.submission.create(db=db)
    alert3_o1 = factory.observable.create_or_read(
        type="ipv4", value="172.16.1.1", parent_analysis=alert3.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="FA Queue Type 1", db=db),
        submission=alert3,
        target=alert3_o1,
        details={"link": "https://url.to.search/query=asdf", "hits": 0},
    )

    # The observable summary should now have two entries in it. Even though the 127.0.0.1 observable was repeated three
    # times across the two alerts, its FA Queue Analysis is going to be the same for each, so it appears once in the summary.
    # Additionally, the results should be sorted by their type then value.
    get = client.get(f"/api/event/{event.uuid}/summary/observable")
    assert len(get.json()) == 2
    assert get.json()[0]["value"] == "127.0.0.1"
    assert get.json()[0]["faqueue_hits"] == 10
    assert get.json()[1]["value"] == "192.168.1.1"
    assert get.json()[1]["faqueue_hits"] == 100


def test_summary_sandbox(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The sandbox summary should be empty
    get = client.get(f"/api/event/{event.uuid}/summary/sandbox")
    assert get.json() == []

    # Define the sandbox analysis details that will be used in the alerts
    sample1_details = SandboxAnalysisDetails(
        contacted_hosts=[
            SandboxContactedHost(
                ip="127.0.0.1",
                port=80,
                protocol="TCP",
                location="some place",
                associated_domains=["domain1", "domain2"],
            ),
            SandboxContactedHost(
                ip="192.168.1.1", port=443, protocol="TCP", location="some other place", associated_domains=[]
            ),
        ],
        created_services=["created_service1", "created_service2"],
        dns_requests=[
            SandboxDnsRequest(request="malware.com", type="A", answer="127.0.0.1", answer_type="A"),
            SandboxDnsRequest(request="othermalware.com", type="A", answer="192.168.1.1", answer_type="A"),
        ],
        dropped_files=[
            SandboxDroppedFile(
                filename="dropped1.exe",
                path="c:\\users\\analyst\\desktop\\dropped1.exe",
                size=100,
                type="application/octet-stream",
                md5="10239eb7264449296277d10538e27f3e",
                sha1="344329cc1356f227a722ad81e36a6e5baf6a0642",
                sha256="17d771db597ca8eb06c874200a067d7ac4374aa14d7b775a3b57181e69cfb100",
                sha512="54f61aba3cfb0249b84b9b2464b946e1039615dbebe6ce2ca6403c91945ef30a6156eb5c3ec330fe8c67b34e8a8b71a2f6e8d394874a72dd06fb96649d020682",
                ssdeep="3:cIoN:cb",
            ),
            SandboxDroppedFile(
                filename="dropped2.exe",
                path="c:\\users\\analyst\\desktop\\dropped2.exe",
                size=100,
                type="application/octet-stream",
                md5="8ad98e2965070ebbb86a95e35c18010f",
                sha1="6e1833d62213441c60edce1a4cfb6674af102d69",
                sha256="fc0fefa8d1f318419f927bc3b793bf66a035d59f24874ce7cf773f9162d0a158",
                sha512="6774d837fb2851c1c1d89170068caa1b81143b81ec7fbf4322b3ffdbc24efcebcc12d763d1c6f4b0c843e43427671453167b1c50ed5f71c7ede8759f75f39732",
                ssdeep="3:cIeAn:ckn",
            ),
        ],
        filename="malware.exe",
        http_requests=[
            SandboxHttpRequest(
                host="malware.com",
                port=80,
                path="/malware.exe",
                method="GET",
                user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
            ),
            SandboxHttpRequest(
                host="othermalware.com",
                port=443,
                path="/othermalware.exe",
                method="GET",
                user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
            ),
        ],
        malware_family="ransomware",
        md5="9051c29972c935649d8fa4b823e54dea",
        memory_strings=["memory_string1", "memory_string2"],
        memory_urls=["http://memory.url1", "http://memory.url2"],
        mutexes=["mutex1", "mutex2"],
        processes=[
            SandboxProcess(command="malware.exe", pid=1000, parent_pid=0),
            SandboxProcess(command="sub_command1", pid=1001, parent_pid=1000),
            SandboxProcess(command="sub_sub_command", pid=1002, parent_pid=1001),
            SandboxProcess(command="sub_command2", pid=1003, parent_pid=1000),
        ],
        registry_keys=["registry_key1", "registry_key2"],
        resolved_apis=["resolved_api1", "resolved_api2"],
        sandbox_url="https://url.to.sandbox.report",
        sha1="2da7b04fa4f6e94c7c82c1c8ee09ead16121bc60",
        sha256="66ecfc29b6d458538b23310988289158f319e2e1cf7587413011d43a639c6ec0",
        sha512="951c56c1bad4cdb721da736d9f1c04ebbbf32d2737c8ec8c64086a4c5448cb37f95784186c8c67c42b7bc622ba6358dc8befee750c14bcf5136a6706a19e007b",
        ssdeep="3:5c+a:q",
        started_services=["started_service1", "started_service2"],
        strings_urls=["https://string.url1", "https://string.url2"],
        suricata_alerts=["suricata_alert1", "suricata_alert2"],
    )

    sample2_details = SandboxAnalysisDetails(
        filename="othermalware.exe",
        md5="be0910beda52d3c1552822c43345061a",
        sandbox_url="https://url.to.other.sandbox.report",
        sha1="534cc9232929857e8b84236a4f955c9b5d303a7d",
        sha256="73b4ed99444440ad52ad2bb8da8ee7d186d4b31705783c0b8f45ada7007bfd1c",
    )

    sample3_details = SandboxAnalysisDetails(
        filename="good.exe",
        md5="93ac743902fa30840d4cd30a52068a78",
        sandbox_url="https://url.to.sandbox.report",
    )

    # Add some alerts with sandbox analysis to the event
    #
    # alert1
    #   o1
    #     a1 - Sandbox Analysis (malware.exe)
    #
    # alert2
    #   o1
    #     a1 - Sandbox Analysis (malware.exe)
    #   o2
    #     a2 - Sandbox Analysis (othermalware.exe)
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="file", value="malware.exe", parent_analysis=alert1.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Sandbox Analysis - Sandbox 1", db=db),
        submission=alert1,
        target=alert1_o1,
        details=json.loads(sample1_details.json()),
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="file", value="malware.exe", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Sandbox Analysis - Sandbox 1", db=db),
        submission=alert2,
        target=alert2_o1,
        details=json.loads(sample1_details.json()),
    )
    alert2_o2 = factory.observable.create_or_read(
        type="file", value="othermalware.exe", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Sandbox Analysis - Sandbox 2", db=db),
        submission=alert2,
        target=alert2_o2,
        details=json.loads(sample2_details.json()),
    )

    # Add a third alert that is not part of the event
    alert3 = factory.submission.create(db=db)
    alert3_o1 = factory.observable.create_or_read(
        type="file", value="good.exe", parent_analysis=alert3.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="Sandbox Analysis - Sandbox 1", db=db),
        submission=alert3,
        target=alert3_o1,
        details=json.loads(sample3_details.json()),
    )

    # The sandbox summary should now have two entries in it. The malware.exe report is repeated, so it
    # only counts once for the purposes of the summary.
    # Additionally, the results should be sorted by the filenames.
    get = client.get(f"/api/event/{event.uuid}/summary/sandbox")
    assert len(get.json()) == 2
    assert get.json()[0]["filename"] == "malware.exe"
    assert get.json()[0]["process_tree"] == "malware.exe\n    sub_command1\n        sub_sub_command\n    sub_command2"
    assert get.json()[1]["filename"] == "othermalware.exe"
    assert get.json()[1]["process_tree"] == ""


def test_summary_url_domains(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The URL domains summary should be empty
    get = client.get(f"/api/event/{event.uuid}/summary/url_domain")
    assert get.json() == {"domains": [], "total": 0}

    # Add some alerts with analyses to the event
    #
    # alert1
    #   o1 - https://example.com
    #     a1
    #       o2 - https://example2.com
    #       o3 - https://example.com
    #
    # alert2
    #  o1 - https://example.com/index.html
    #  o2 - https://example3.com
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="url", value="https://example.com", parent_analysis=alert1.root_analysis, db=db
    )
    alert1_a1 = factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="URL Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
    )
    factory.observable.create_or_read(type="url", value="https://example2.com", parent_analysis=alert1_a1, db=db)
    factory.observable.create_or_read(type="url", value="https://example.com", parent_analysis=alert1_a1, db=db)

    alert2 = factory.submission.create(db=db, event=event)
    factory.observable.create_or_read(
        type="url", value="https://example.com/index.html", parent_analysis=alert2.root_analysis, db=db
    )
    factory.observable.create_or_read(
        type="url", value="https://example3.com", parent_analysis=alert2.root_analysis, db=db
    )

    # Add a third alert that is not part of the event
    alert3 = factory.submission.create(db=db)
    factory.observable.create_or_read(
        type="url", value="https://example4.com", parent_analysis=alert3.root_analysis, db=db
    )

    # The URL domain summary should now have three entries in it. The https://example.com URL is repeated, so it
    # only counts once for the purposes of the summary.
    # Additionally, the results should be sorted by the number of times the domains appeared then by the domain.
    #
    # Results: example.com (2), example2.com (1), example3.com (1)
    get = client.get(f"/api/event/{event.uuid}/summary/url_domain")
    assert get.json()["total"] == 4
    assert len(get.json()["domains"]) == 3
    assert get.json()["domains"][0]["domain"] == "example.com"
    assert get.json()["domains"][0]["count"] == 2
    assert get.json()["domains"][1]["domain"] == "example2.com"
    assert get.json()["domains"][1]["count"] == 1
    assert get.json()["domains"][2]["domain"] == "example3.com"
    assert get.json()["domains"][2]["count"] == 1


def test_summary_user(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The user summary should be empty
    get = client.get(f"/api/event/{event.uuid}/summary/user")
    assert get.json() == []

    # Add some alerts with analyses to the event
    #
    # alert1
    #   o1
    #     a1 - user1 analysis
    #
    # alert2
    #  o1
    #    a1 - user2 analysis
    #
    # alert3
    #  o1
    #    a1 - user1 analysis

    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="email_address", value="goodguy@company.com", parent_analysis=alert1.root_analysis, db=db
    )
    # This analysis is missing the optional "manager_email" key
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="User Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
        details={
            "user_id": "12345",
            "email": "goodguy@company.com",
            "company": "Company Inc.",
            "division": "R&D",
            "department": "Widgets",
            "title": "Director",
        },
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="email_address", value="otherguy@company.com", parent_analysis=alert2.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="User Analysis", db=db),
        submission=alert2,
        target=alert2_o1,
        details={
            "user_id": "98765",
            "email": "otherguy@company.com",
            "company": "Company Inc.",
            "division": "R&D",
            "department": "Widgets",
            "title": "Engineer",
            "manager_email": "goodguy@company.com",
        },
    )

    alert3 = factory.submission.create(db=db, event=event)
    alert3_o1 = factory.observable.create_or_read(
        type="email_address", value="goodguy@company.com", parent_analysis=alert3.root_analysis, db=db
    )
    # This analysis is missing the optional "manager_email" key
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="User Analysis", db=db),
        submission=alert3,
        target=alert3_o1,
        details={
            "user_id": "12345",
            "email": "goodguy@company.com",
            "company": "Company Inc.",
            "division": "R&D",
            "department": "Widgets",
            "title": "Director",
        },
    )

    # Add a fourth alert that is not part of the event
    alert4 = factory.submission.create(db=db)
    alert4_o1 = factory.observable.create_or_read(
        type="email_address", value="dude@company.com", parent_analysis=alert4.root_analysis, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="User Analysis", db=db),
        submission=alert4,
        target=alert4_o1,
        details={
            "user_id": "abcde",
            "email": "dude@company.com",
            "company": "Company Inc.",
            "division": "Finance",
            "department": "Widgets",
            "title": "Accountant",
            "manager_email": "manager@company.com",
        },
    )

    # The user summary should now have two entries in it. Even though one user's analysis was repeated two
    # times across the alerts, its User Analysis is going to be the same for each, so it appears once in the summary.
    # Additionally, the results should be sorted by their email.
    get = client.get(f"/api/event/{event.uuid}/summary/user")
    assert len(get.json()) == 2
    assert get.json()[0]["email"] == "goodguy@company.com"
    assert get.json()[0]["manager_email"] is None
    assert get.json()[1]["email"] == "otherguy@company.com"


def test_analysis_module_types(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The list of analysis types should be empty
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["analysis_types"] == []

    # Add some alerts with analyses to the event
    alert1 = factory.submission.create(db=db, event=event)
    alert1_o1 = factory.observable.create_or_read(
        type="url", value="https://127.0.0.1", parent_analysis=alert1.root_analysis, db=db
    )
    alert1_a1 = factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="URL Analysis", db=db),
        submission=alert1,
        target=alert1_o1,
    )
    alert1_o2 = factory.observable.create_or_read(type="ipv4", value="127.0.0.1", parent_analysis=alert1_a1, db=db)
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="IP Analysis", db=db),
        submission=alert1,
        target=alert1_o2,
    )

    alert2 = factory.submission.create(db=db, event=event)
    alert2_o1 = factory.observable.create_or_read(
        type="url", value="https://127.0.0.1/malware.exe", parent_analysis=alert2.root_analysis, db=db
    )
    alert2_a1 = factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="URL Analysis", db=db),
        submission=alert2,
        target=alert2_o1,
    )
    alert2_o2 = factory.observable.create_or_read(
        type="uri_path", value="/malware.exe", parent_analysis=alert2_a1, db=db
    )
    factory.analysis.create_or_read(
        db=db,
        analysis_module_type=factory.analysis_module_type.create_or_read(value="URI Path Analysis", db=db),
        submission=alert2,
        target=alert2_o2,
    )

    # The list of analysis types should now have some entries
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["analysis_types"] == ["IP Analysis", "URI Path Analysis", "URL Analysis"]


def test_auto_alert_time(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The auto_alert_time should be empty
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["auto_alert_time"] is None

    # Add an alert to the event
    now = datetime.utcnow()
    alert1 = factory.submission.create(db=db, event=event, insert_time=now)

    # Verify the auto_alert_time
    get = client.get(f"/api/event/{event.uuid}")
    assert parse(get.json()["auto_alert_time"]).timestamp() == alert1.insert_time.timestamp()

    # Add a second alert to the event with an earlier insert time
    earlier = now - timedelta(seconds=5)
    alert2 = factory.submission.create(db=db, event=event, insert_time=earlier)

    # Verify the new auto_alert_time
    get = client.get(f"/api/event/{event.uuid}")
    assert parse(get.json()["auto_alert_time"]).timestamp() == alert2.insert_time.timestamp()


def test_auto_disposition_time(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The auto_disposition_time should be empty
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["auto_disposition_time"] is None

    # Add an alert to the event
    now = datetime.utcnow()
    alert1 = factory.submission.create(
        db=db, event=event, disposition="DELIVERY", update_time=now, history_username="analyst"
    )

    # Verify the auto_disposition_time
    get = client.get(f"/api/event/{event.uuid}")
    assert parse(get.json()["auto_disposition_time"]) == alert1.disposition_time_earliest

    # Add a second alert to the event with an earlier disposition time
    earlier = now - timedelta(seconds=5)
    alert2 = factory.submission.create(
        db=db, event=event, disposition="DELIVERY", update_time=earlier, history_username="analyst"
    )

    # Verify the new auto_disposition_time
    get = client.get(f"/api/event/{event.uuid}")
    assert parse(get.json()["auto_disposition_time"]) == alert2.disposition_time_earliest


def test_auto_event_time(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The auto_event_time should be empty
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["auto_event_time"] is None

    # Add an alert to the event
    now = datetime.utcnow()
    alert1 = factory.submission.create(db=db, event=event, event_time=now)

    # Verify the auto_event_time
    get = client.get(f"/api/event/{event.uuid}")
    assert parse(get.json()["auto_event_time"]).timestamp() == alert1.event_time.timestamp()

    # Add a second alert to the event with an earlier insert time
    earlier = now - timedelta(seconds=5)
    alert2 = factory.submission.create(db=db, event=event, event_time=earlier)

    # Verify the new auto_event_time
    get = client.get(f"/api/event/{event.uuid}")
    assert parse(get.json()["auto_event_time"]).timestamp() == alert2.event_time.timestamp()


def test_auto_ownership_time(client, db):
    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The auto_ownership_time should be empty
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["auto_ownership_time"] is None

    # Add an alert to the event
    now = datetime.utcnow()
    alert1 = factory.submission.create(db=db, event=event, owner="alice", update_time=now, history_username="analyst")

    # Verify the auto_ownership_time
    get = client.get(f"/api/event/{event.uuid}")
    assert parse(get.json()["auto_ownership_time"]) == alert1.ownership_time_earliest

    # Add a second alert to the event with an earlier ownership time
    earlier = now - timedelta(seconds=5)
    alert2 = factory.submission.create(
        db=db, event=event, owner="alice", update_time=earlier, history_username="analyst"
    )

    # Verify the new auto_ownership_time
    get = client.get(f"/api/event/{event.uuid}")
    assert parse(get.json()["auto_ownership_time"]) == alert2.ownership_time_earliest


def test_disposition(client, db):
    # Create some dispositions
    factory.alert_disposition.create_or_read(value="FALSE_POSITIVE", rank=1, db=db)
    factory.alert_disposition.create_or_read(value="DELIVERY", rank=2, db=db)

    # Create an event
    event = factory.event.create_or_read(name="test event", db=db)

    # The disposition should be empty
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["disposition"] is None

    # Add an alert to the event
    factory.submission.create(db=db, event=event, disposition="FALSE_POSITIVE")

    # Verify the disposition
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["disposition"]["value"] == "FALSE_POSITIVE"

    # Add a second alert to the event with a higher disposition
    factory.submission.create(db=db, event=event, disposition="DELIVERY")

    # Verify the new disposition
    get = client.get(f"/api/event/{event.uuid}")
    assert get.json()["disposition"]["value"] == "DELIVERY"


def test_get_all_pagination(client, db):
    # Create 11 events
    for i in range(11):
        factory.event.create_or_read(name=f"event{i}", db=db)

    # Keep track of all of the event UUIDs to make sure we read them all
    unique_event_uuids = set()

    # Read every page in chunks of 2 while there are still results
    offset = 0
    while True:
        get = client.get(f"/api/event/?limit=2&offset={offset}")

        # Store the event UUIDs
        for event in get.json()["items"]:
            unique_event_uuids.add(event["uuid"])

            # Make sure the node_type field is "event"
            assert event["node_type"] == "event"

        # Check if there is another page to retrieve
        if len(unique_event_uuids) < get.json()["total"]:
            # Increase the offset to get the next page
            offset += get.json()["limit"]
            continue

        break

    # Should have gotten all 11 events across the pages
    assert len(unique_event_uuids) == 11


def test_get_all_empty(client):
    get = client.get("/api/event/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {"items": [], "limit": 50, "offset": 0, "total": 0}


def test_get_filter_alert_time_after(client, db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    alert1 = factory.submission.create(event=event1, insert_time=datetime.utcnow() - timedelta(seconds=5), db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(event=event2, insert_time=datetime.utcnow(), db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(event=event3, insert_time=datetime.utcnow() + timedelta(seconds=5), db=db)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by alert_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"alert_time_after": alert2.insert_time}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"
    assert parse(get.json()["items"][0]["auto_alert_time"]) == alert3.insert_time

    params2 = {"alert_time_after": alert1.insert_time}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_alert_time_before(client, db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    alert1 = factory.submission.create(event=event1, insert_time=datetime.utcnow() - timedelta(seconds=5), db=db)

    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(event=event2, insert_time=datetime.utcnow(), db=db)

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(event=event3, insert_time=datetime.utcnow() + timedelta(seconds=5), db=db)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by alert_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"alert_time_before": alert2.insert_time}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"
    assert parse(get.json()["items"][0]["auto_alert_time"]) == alert1.insert_time

    params2 = {"alert_time_before": alert3.insert_time}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_contain_time_after(client, db):
    event1 = factory.event.create_or_read(name="event1", contain_time=datetime.utcnow() - timedelta(seconds=5), db=db)
    event2 = factory.event.create_or_read(name="event2", contain_time=datetime.utcnow(), db=db)
    event3 = factory.event.create_or_read(name="event3", contain_time=datetime.utcnow() + timedelta(seconds=5), db=db)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by contain_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"contain_time_after": event2.contain_time}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"

    params2 = {"contain_time_after": event1.contain_time}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_contain_time_before(client, db):
    event1 = factory.event.create_or_read(name="event1", contain_time=datetime.utcnow() - timedelta(seconds=5), db=db)
    event2 = factory.event.create_or_read(name="event2", contain_time=datetime.utcnow(), db=db)
    event3 = factory.event.create_or_read(name="event3", contain_time=datetime.utcnow() + timedelta(seconds=5), db=db)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by contain_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"contain_time_before": event2.contain_time}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"

    params2 = {"contain_time_before": event3.contain_time}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_created_time_after(client, db):
    event1 = factory.event.create_or_read(name="event1", created_time=datetime.utcnow() - timedelta(seconds=5), db=db)
    event2 = factory.event.create_or_read(name="event2", created_time=datetime.utcnow(), db=db)
    event3 = factory.event.create_or_read(name="event3", created_time=datetime.utcnow() + timedelta(seconds=5), db=db)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by created_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"created_time_after": event2.created_time}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"

    params2 = {"created_time_after": event1.created_time}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_created_time_before(client, db):
    event1 = factory.event.create_or_read(name="event1", created_time=datetime.utcnow() - timedelta(seconds=5), db=db)
    event2 = factory.event.create_or_read(name="event2", created_time=datetime.utcnow(), db=db)
    event3 = factory.event.create_or_read(name="event3", created_time=datetime.utcnow() + timedelta(seconds=5), db=db)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by created_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"created_time_before": event2.created_time}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"

    params2 = {"created_time_before": event3.created_time}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_disposition(client, db):
    event1 = factory.event.create_or_read(name="event1", contain_time=datetime.utcnow() - timedelta(seconds=5), db=db)
    factory.submission.create(event=event1, db=db)

    event2 = factory.event.create_or_read(name="event2", contain_time=datetime.utcnow(), db=db)
    factory.submission.create(event=event2, db=db, disposition="FALSE_POSITIVE")

    # There should be 2 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 2

    # There should only be 1 event when we filter by the disposition
    get = client.get("/api/event/?disposition=none")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"

    get = client.get("/api/event/?disposition=FALSE_POSITIVE")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event2"

    get = client.get("/api/event/?disposition=FALSE_POSITIVE&disposition=none")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_disposition_time_after(client, db):
    now = datetime.utcnow()

    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(
        event=event1, disposition="DELIVERY", update_time=now - timedelta(seconds=5), db=db, history_username="analyst"
    )

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(event=event2, disposition="DELIVERY", update_time=now, db=db, history_username="analyst")

    event3 = factory.event.create_or_read(name="event3", db=db)
    factory.submission.create(
        event=event3, disposition="DELIVERY", update_time=now + timedelta(seconds=5), db=db, history_username="analyst"
    )

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by disposition_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"disposition_time_after": now}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"

    params2 = {"disposition_time_after": now - timedelta(seconds=5)}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_disposition_time_before(client, db):
    now = datetime.utcnow()

    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(
        event=event1, disposition="DELIVERY", update_time=now - timedelta(seconds=5), db=db, history_username="analyst"
    )

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(event=event2, disposition="DELIVERY", update_time=now, db=db, history_username="analyst")

    event3 = factory.event.create_or_read(name="event3", db=db)
    factory.submission.create(
        event=event3, disposition="DELIVERY", update_time=now + timedelta(seconds=5), db=db, history_username="analyst"
    )

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by disposition_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"disposition_time_before": now}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"

    params2 = {"disposition_time_before": now + timedelta(seconds=5)}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_event_type(client, db):
    event1 = factory.event.create_or_read(name="event1", db=db, event_type="test_type")
    event2 = factory.event.create_or_read(name="event2", db=db, event_type="test_type2")

    # There should be 2 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 2

    # There should only be 1 event when we filter by test_type
    get = client.get("/api/event/?event_type=test_type")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["type"]["value"] == "test_type"

    # There should be 2 total events when we filter by test_type1 and test_type2
    get = client.get("/api/event/?event_type=test_type&event_type=test_type2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_name(client, db):
    event1 = factory.event.create_or_read(db=db, name="Test Event")
    event2 = factory.event.create_or_read(db=db, name="Some Other Event")

    # There should be 2 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 2

    # There should only be 1 event when we filter by the name
    get = client.get("/api/event/?name=test")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "Test Event"

    # There should be 2 total events when we filter by both names
    get = client.get("/api/event/?name=test&name=other")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_observable(client, db):
    # Create an empty event
    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(db=db, event=event1)

    # Create some events with one observable
    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(db=db, event=event2)
    factory.observable.create_or_read(
        parent_analysis=alert2.root_analysis, type="test_type1", value="test_value1", db=db
    )

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(db=db, event=event3)
    factory.observable.create_or_read(
        parent_analysis=alert3.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # Create an event with multiple observables
    event4 = factory.event.create_or_read(name="event4", db=db)
    alert4 = factory.submission.create(db=db, event=event4)
    factory.observable.create_or_read(
        parent_analysis=alert4.root_analysis, type="test_type1", value="test_value_asdf", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=alert4.root_analysis, type="test_type2", value="test_value1", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=alert4.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # There should be 4 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 4

    # There should only be 1 event when we filter by the test_type1/test_value1 observable
    get = client.get("/api/event/?observable=test_type1|test_value1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event2"

    # There should be 2 events when we filter by the test_type2/test_value2 observable
    get = client.get("/api/event/?observable=test_type2|test_value2")
    assert get.json()["total"] == 2
    assert any(a["name"] == "event3" for a in get.json()["items"])
    assert any(a["name"] == "event4" for a in get.json()["items"])

    # There should be 3 events when we filter by the test_type1/test_value1 and test_type2/test_value2 observable
    get = client.get("/api/event/?observable=test_type1|test_value1&observable=test_type2|test_value2")
    assert get.json()["total"] == 3
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event4.uuid) for a in get.json()["items"])


def test_get_filter_observable_types(client, db):
    # Create an empty event
    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(db=db, event=event1)

    # Create an event with one observable
    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(db=db, event=event2)
    factory.observable.create_or_read(
        parent_analysis=alert2.root_analysis, type="test_type1", value="test_value1", db=db
    )

    # Create an alert with multiple observables
    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(db=db, event=event3)
    factory.observable.create_or_read(
        parent_analysis=alert3.root_analysis, type="test_type1", value="test_value_asdf", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=alert3.root_analysis, type="test_type2", value="test_value1", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=alert3.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should be 2 events when we filter by just test_type1
    get = client.get("/api/event/?observable_types=test_type1")
    assert get.json()["total"] == 2
    assert any(a["name"] == "event2" for a in get.json()["items"])
    assert any(a["name"] == "event3" for a in get.json()["items"])

    # There should only be 1 event when we filter by the test_type1 and test_type2
    get = client.get("/api/event/?observable_types=test_type1,test_type2")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"

    # There should be 2 events when we filter by (test_type1 and test_type2) or just test_type1
    get = client.get("/api/event/?observable_types=test_type1,test_type2&observable_types=test_type1")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_observable_value(client, db):
    # Create an empty event
    event1 = factory.event.create_or_read(name="event1", db=db)
    factory.submission.create(db=db, event=event1)

    # Create some alerts with one observable
    event2 = factory.event.create_or_read(name="event2", db=db)
    alert2 = factory.submission.create(db=db, event=event2)
    factory.observable.create_or_read(
        parent_analysis=alert2.root_analysis, type="test_type1", value="test_value1", db=db
    )

    event3 = factory.event.create_or_read(name="event3", db=db)
    alert3 = factory.submission.create(db=db, event=event3)
    factory.observable.create_or_read(
        parent_analysis=alert3.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # Create an event with multiple observables
    event4 = factory.event.create_or_read(name="event4", db=db)
    alert4 = factory.submission.create(db=db, event=event4)
    factory.observable.create_or_read(
        parent_analysis=alert4.root_analysis, type="test_type1", value="test_value_asdf", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=alert4.root_analysis, type="test_type2", value="test_value1", db=db
    )
    factory.observable.create_or_read(
        parent_analysis=alert4.root_analysis, type="test_type2", value="test_value2", db=db
    )

    # There should be 4 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 4

    # There should only be 1 event when we filter by the test_value_asdf observable value
    get = client.get("/api/event/?observable_value=test_value_asdf")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event4"

    # There should be 2 events when we filter by the test_value1 observable value
    get = client.get("/api/event/?observable_value=test_value1")
    assert get.json()["total"] == 2
    assert any(a["name"] == "event2" for a in get.json()["items"])
    assert any(a["name"] == "event4" for a in get.json()["items"])

    # There should be 3 events when we filter by the test_value1 and test_value2 observable value
    get = client.get("/api/event/?observable_value=test_value1&observable_value=test_value2")
    assert get.json()["total"] == 3
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event4.uuid) for a in get.json()["items"])


def test_get_filter_owner(client, db):
    factory.user.create_or_read(username="analyst", db=db)
    event1 = factory.event.create_or_read(name="event1", db=db)
    event2 = factory.event.create_or_read(name="event2", db=db, owner="analyst")

    # There should be 2 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 2

    # There should only be 1 event when we filter by the owner
    get = client.get("/api/event/?owner=analyst")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["owner"]["username"] == "analyst"

    # There should be 2 events when we filter by owner and none
    get = client.get("/api/event/?owner=analyst&owner=none")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_prevention_tools(client, db):
    factory.event.create_or_read(name="event1", db=db)
    event2 = factory.event.create_or_read(name="event2", db=db, prevention_tools=["value1"])
    event3 = factory.event.create_or_read(name="event3", db=db, prevention_tools=["value2", "value3"])

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by value1
    get = client.get("/api/event/?prevention_tools=value1")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["prevention_tools"]) == 1
    assert get.json()["items"][0]["prevention_tools"][0]["value"] == "value1"

    # There should only be 1 event when we filter by value2 AND value3
    get = client.get("/api/event/?prevention_tools=value2,value3")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["prevention_tools"]) == 2
    assert any(t["value"] == "value2" for t in get.json()["items"][0]["prevention_tools"])
    assert any(t["value"] == "value3" for t in get.json()["items"][0]["prevention_tools"])

    # There should be 2 events when we filter by value1 OR (value2 AND value3)
    get = client.get("/api/event/?prevention_tools=value1&prevention_tools=value2,value3")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_queue(client, db):
    event1 = factory.event.create_or_read(name="event1", db=db, event_queue="test_queue1")
    event2 = factory.event.create_or_read(name="event2", db=db, event_queue="test_queue2")

    # There should be 2 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 2

    # There should only be 1 event when we filter by the queue
    get = client.get("/api/event/?queue=test_queue1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["queue"]["value"] == "test_queue1"

    # There should be 2 events when we filter by two different queues
    get = client.get("/api/event/?queue=test_queue1&queue=test_queue2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_remediation_time_after(client, db):
    event1 = factory.event.create_or_read(
        name="event1", remediation_time=datetime.utcnow() - timedelta(seconds=5), db=db
    )
    event2 = factory.event.create_or_read(name="event2", remediation_time=datetime.utcnow(), db=db)
    event3 = factory.event.create_or_read(
        name="event3", remediation_time=datetime.utcnow() + timedelta(seconds=5), db=db
    )

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by remediation_time_after. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"remediation_time_after": event2.remediation_time}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"

    params2 = {"remediation_time_after": event1.remediation_time}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_remediation_time_before(client, db):
    event1 = factory.event.create_or_read(
        name="event1", remediation_time=datetime.utcnow() - timedelta(seconds=5), db=db
    )
    event2 = factory.event.create_or_read(name="event2", remediation_time=datetime.utcnow(), db=db)
    event3 = factory.event.create_or_read(
        name="event3", remediation_time=datetime.utcnow() + timedelta(seconds=5), db=db
    )

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by remediation_time_before. But the timestamp
    # has a timezone specified, which uses the + symbol that needs to be urlencoded since it
    # is a reserved URL character.
    params1 = {"remediation_time_before": event2.remediation_time}
    get = client.get(f"/api/event/?{urlencode(params1)}")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"

    params2 = {"remediation_time_before": event3.remediation_time}
    get = client.get(f"/api/event/?{urlencode(params1)}&{urlencode(params2)}")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event1.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])


def test_get_filter_remediations(client, db):
    factory.event.create_or_read(name="event1", db=db)
    event2 = factory.event.create_or_read(name="event2", db=db, remediations=["value1"])
    event3 = factory.event.create_or_read(name="event3", db=db, remediations=["value2", "value3"])

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by value1
    get = client.get("/api/event/?remediations=value1")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["remediations"]) == 1
    assert get.json()["items"][0]["remediations"][0]["value"] == "value1"

    # There should only be 1 event when we filter by value2 AND value3
    get = client.get("/api/event/?remediations=value2,value3")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["remediations"]) == 2
    assert any(t["value"] == "value2" for t in get.json()["items"][0]["remediations"])
    assert any(t["value"] == "value3" for t in get.json()["items"][0]["remediations"])

    # There should 2 events when we filter by value1 OR (value2 AND value3)
    get = client.get("/api/event/?remediations=value1&remediations=value2,value3")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_severity(client, db):
    factory.event.create_or_read(name="event1", db=db)
    event2 = factory.event.create_or_read(name="event2", db=db, severity="value1")
    event3 = factory.event.create_or_read(name="event3", db=db, severity="value2")

    # There should be 2 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by value1
    get = client.get("/api/event/?severity=value1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["severity"]["value"] == "value1"

    # There should 2 events when we filter by value1 OR value2
    get = client.get("/api/event/?severity=value1&severity=value2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_source(client, db):
    factory.event.create_or_read(name="event1", db=db)
    event2 = factory.event.create_or_read(name="event2", db=db, source="value1")
    event3 = factory.event.create_or_read(name="event3", db=db, source="value2")

    # There should be 2 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by value1
    get = client.get("/api/event/?source=value1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["source"]["value"] == "value1"

    # There should 2 events when we filter by value1 OR value2
    get = client.get("/api/event/?source=value1&source=value2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_status(client, db):
    factory.event.create_or_read(name="event1", db=db, status="value1")
    event2 = factory.event.create_or_read(name="event2", db=db, status="value2")
    event3 = factory.event.create_or_read(name="event3", db=db, status="value3")

    # There should be 2 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by value1
    get = client.get("/api/event/?status=value1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["status"]["value"] == "value1"

    # There should 2 events when we filter by value1 OR value2
    get = client.get("/api/event/?status=value2&status=value3")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_tags(client, db):
    # Create an event with a tagged observable
    event1 = factory.event.create_or_read(name="event1", db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(
        type="fqdn", value="bad.com", parent_analysis=alert1.root_analysis, db=db, analysis_tags=["obs1"]
    )

    # Create an event with an alert with one tag
    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(event=event2, db=db, tags=["tag1"])

    # Create an event with an alert with two tags
    event3 = factory.event.create_or_read(name="event3", db=db)
    factory.submission.create(event=event3, db=db, tags=["tag2", "tag3"])

    # Create a tagged event
    event4 = factory.event.create_or_read(name="event4", db=db, tags=["tag4"])
    factory.submission.create(event=event4, db=db)

    # There should be 4 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 4

    # There should only be 1 event when we filter by tag1
    get = client.get("/api/event/?tags=tag1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event2"

    # There should only be 1 event when we filter by tag2 AND tag3
    get = client.get("/api/event/?tags=tag2,tag3")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"

    # There should only be 1 event when we filter by the child observable tag obs1
    get = client.get("/api/event/?tags=obs1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"

    # There should only be 1 event when we filter by tag4
    get = client.get("/api/event/?tags=tag4")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event4"

    # There should be 2 events when we filter by tag1 OR (tag2 AND tag3)
    get = client.get("/api/event/?tags=tag1&tags=tag2,tag3")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_threat_actors(client, db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(
        type="fqdn", value="bad.com", parent_analysis=alert1.root_analysis, db=db, threat_actors=["bad_guys"]
    )

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(event=event2, db=db, threat_actors=["test_actor"])

    event3 = factory.event.create_or_read(name="event3", db=db, threat_actors=["test_actor2"])
    factory.submission.create(event=event3, db=db)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should be 1 event when we filter test_actor
    get = client.get("/api/event/?threat_actors=test_actor")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event2"

    # There should be 1 event when we filter by the child observable threat_actor
    get = client.get("/api/event/?threat_actors=bad_guys")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"

    # There should be 1 event when we filter test_actor2
    get = client.get("/api/event/?threat_actors=test_actor2")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"

    # There should be 2 events when we filter by test_actor OR test_actor2
    get = client.get("/api/event/?threat_actors=test_actor&threat_actors=test_actor2")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_threats(client, db):
    event1 = factory.event.create_or_read(name="event1", db=db)
    alert1 = factory.submission.create(event=event1, db=db)
    factory.observable.create_or_read(
        type="fqdn", value="bad.com", parent_analysis=alert1.root_analysis, db=db, threats=["malz"]
    )

    event2 = factory.event.create_or_read(name="event2", db=db)
    factory.submission.create(event=event2, db=db, threats=["threat1"])

    event3 = factory.event.create_or_read(name="event3", db=db, threats=["threat2", "threat3"])
    factory.submission.create(event=event3, db=db)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should be 1 event when we filter by threat1
    get = client.get("/api/event/?threats=threat1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event2"

    # There should be 1 event when we filter by the child observable threat
    get = client.get("/api/event/?threats=malz")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event1"

    # There should be 1 event when we filter by threat2 AND threat3
    get = client.get("/api/event/?threats=threat2,threat3")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event3"

    # There should be 2 events when we filter by threat1 OR (threat2 AND threat3)
    get = client.get("/api/event/?threats=threat1&threats=threat2,threat3")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_filter_vectors(client, db):
    factory.event.create_or_read(name="event1", db=db)
    event2 = factory.event.create_or_read(name="event2", db=db, vectors=["value1"])
    event3 = factory.event.create_or_read(name="event3", db=db, vectors=["value2", "value3"])

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by value1
    get = client.get("/api/event/?vectors=value1")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["vectors"]) == 1
    assert get.json()["items"][0]["vectors"][0]["value"] == "value1"

    # There should only be 1 event when we filter by value2 AND value3
    get = client.get("/api/event/?vectors=value2,value3")
    assert get.json()["total"] == 1
    assert len(get.json()["items"][0]["vectors"]) == 2
    assert any(t["value"] == "value2" for t in get.json()["items"][0]["vectors"])
    assert any(t["value"] == "value3" for t in get.json()["items"][0]["vectors"])

    # There should be 2 events when we filter by value1 OR (value2 AND value3)
    get = client.get("/api/event/?vectors=value1&vectors=value2,value3")
    assert get.json()["total"] == 2
    assert any(a["uuid"] == str(event2.uuid) for a in get.json()["items"])
    assert any(a["uuid"] == str(event3.uuid) for a in get.json()["items"])


def test_get_multiple_filters(client, db):
    event1 = factory.event.create_or_read(name="event1", db=db, event_type="test_type1")
    factory.submission.create(db=db, event=event1)

    event2 = factory.event.create_or_read(name="event2", db=db, event_type="test_type1", prevention_tools=["tool1"])
    factory.submission.create(db=db, event=event2)

    event2 = factory.event.create_or_read(name="event2", db=db, event_type="test_type2")
    factory.submission.create(db=db, event=event2)

    # There should be 3 total events
    get = client.get("/api/event/")
    assert get.json()["total"] == 3

    # There should only be 1 event when we filter by the type and prevention_tools
    get = client.get("/api/event/?type=test_type1&prevention_tools=tool1")
    assert get.json()["total"] == 1
    assert get.json()["items"][0]["name"] == "event2"


def test_get_sort_by_created_time(client, db):
    factory.event.create_or_read(name="event1", db=db, created_time=datetime.utcnow())
    factory.event.create_or_read(name="event2", db=db, created_time=datetime.utcnow() + timedelta(seconds=5))

    # If you sort descending, the newest event (event2) should appear first
    get = client.get("/api/event/?sort=created_time|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["name"] == "event2"
    assert get.json()["items"][1]["name"] == "event1"

    # If you sort ascending, the oldest event (event1) should appear first
    get = client.get("/api/event/?sort=created_time|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["name"] == "event1"
    assert get.json()["items"][1]["name"] == "event2"


def test_get_sort_by_event_type(client, db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db, event_type="value1")
    factory.event.create_or_read(name="event3", db=db, event_type="value2")

    # If you sort descending: event1, event3, event2
    get = client.get("/api/event/?sort=event_type|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["name"] == "event1"
    assert get.json()["items"][1]["name"] == "event3"
    assert get.json()["items"][2]["name"] == "event2"

    # If you sort ascending: event2, event3, event1
    get = client.get("/api/event/?sort=event_type|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["name"] == "event2"
    assert get.json()["items"][1]["name"] == "event3"
    assert get.json()["items"][2]["name"] == "event1"


def test_get_sort_by_name(client, db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db)

    # If you sort descending: event2, event1
    get = client.get("/api/event/?sort=name|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["name"] == "event2"
    assert get.json()["items"][1]["name"] == "event1"

    # If you sort ascending: event1, event2
    get = client.get("/api/event/?sort=name|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["name"] == "event1"
    assert get.json()["items"][1]["name"] == "event2"


def test_get_sort_by_owner(client, db):
    factory.event.create_or_read(name="event1", db=db, owner="alice")
    factory.event.create_or_read(name="event2", db=db, owner="bob")

    # If you sort descending: event2, event1
    get = client.get("/api/event/?sort=owner|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["name"] == "event2"
    assert get.json()["items"][1]["name"] == "event1"

    # If you sort ascending: event1, event2
    get = client.get("/api/event/?sort=owner|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["name"] == "event1"
    assert get.json()["items"][1]["name"] == "event2"


def test_get_sort_by_severity(client, db):
    factory.event.create_or_read(name="event1", db=db)
    factory.event.create_or_read(name="event2", db=db, severity="value1")
    factory.event.create_or_read(name="event3", db=db, severity="value2")

    # If you sort descending: event1, event3, event2
    get = client.get("/api/event/?sort=severity|desc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["name"] == "event1"
    assert get.json()["items"][1]["name"] == "event3"
    assert get.json()["items"][2]["name"] == "event2"

    # If you sort ascending: event2, event3, event1
    get = client.get("/api/event/?sort=severity|asc")
    assert get.json()["total"] == 3
    assert get.json()["items"][0]["name"] == "event2"
    assert get.json()["items"][1]["name"] == "event3"
    assert get.json()["items"][2]["name"] == "event1"


def test_get_sort_by_status(client, db):
    factory.event.create_or_read(name="event1", db=db, status="value1")
    factory.event.create_or_read(name="event2", db=db, status="value2")

    # If you sort descending: event2, event1
    get = client.get("/api/event/?sort=status|desc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["name"] == "event2"
    assert get.json()["items"][1]["name"] == "event1"

    # If you sort ascending: event1, event2
    get = client.get("/api/event/?sort=status|asc")
    assert get.json()["total"] == 2
    assert get.json()["items"][0]["name"] == "event1"
    assert get.json()["items"][1]["name"] == "event2"
