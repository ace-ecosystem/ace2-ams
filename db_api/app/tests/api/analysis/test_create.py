import json
import pytest
import time
import uuid

from datetime import datetime
from fastapi import HTTPException, status
from api_models.analysis import AnalysisCreate

from db import crud
from tests import factory


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("analysis_module_type_uuid", 123),
        ("analysis_module_type_uuid", None),
        ("analysis_module_type_uuid", ""),
        ("analysis_module_type_uuid", "abc"),
        ("child_observables", 123),
        ("child_observables", None),
        ("child_observables", ""),
        ("child_observables", [123]),
        ("child_observables", [None]),
        ("child_observables", [""]),
        ("child_observables", ["abc", 123]),
        ("child_observables", [{}]),
        ("child_observables", [{"type": "", "value": ""}]),
        ("details", 123),
        ("details", ""),
        ("details", "abc"),
        ("details", []),
        ("error_message", 123),
        ("error_message", ""),
        ("run_time", None),
        ("run_time", ""),
        ("run_time", "Monday"),
        ("run_time", "2022-01-01"),
        ("stack_trace", 123),
        ("stack_trace", ""),
        ("submission_uuid", 123),
        ("submission_uuid", None),
        ("submission_uuid", ""),
        ("submission_uuid", "abc"),
        ("summary", 123),
        ("summary", ""),
        ("target_uuid", 123),
        ("target_uuid", None),
        ("target_uuid", ""),
        ("target_uuid", "abc"),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {
        "analysis_module_type_uuid": str(uuid.uuid4()),
        "submission_uuid": str(uuid.uuid4()),
        "run_time": str(crud.helpers.utcnow()),
        "target_uuid": str(uuid.uuid4()),
    }
    create_json[key] = value
    create = client.post("/api/analysis/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(create.json()["detail"]) >= 1
    assert key in create.json()["detail"][0]["loc"]


def test_create_nonexistent_analysis_module_type(client, db):
    alert = factory.alert.create(db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(uuid.uuid4()),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
        },
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_nonexistent_submission(client, db):
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test_type", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(uuid.uuid4()),
            "target_uuid": str(observable.uuid),
        },
    )

    # The create_analysis API endpoint does not try to read the parent observable, so it returns an
    # IntegrityError and 409 status code if you try to add an analysis with a nonexistent parent observable.
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_invalid_email_analysis(client, db):
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="Email Analysis", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    # Create the analysis - it is missing the required "from_address" key
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "details": json.dumps(
                {
                    "attachments": [],
                    "cc_addresses": [],
                    "headers": "blah",
                    "message_id": "<abcd1234@evil.com>",
                    "subject": "Hello",
                    "time": datetime.now().isoformat(),
                    "to_address": "goodguy@company.com",
                    "extra_field": "extra_value",
                }
            ),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


def test_create_invalid_faqueue_analysis(client, db):
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(
        value="FA Queue Analysis", version="1.0.0", db=db
    )
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    # Create the analysis - it is missing the required "hits" key
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "details": json.dumps({"faqueue_hits": 100, "link": "https://example.com"}),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


def test_create_invalid_sandbox_analysis(client, db):
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="Sandbox Analysis", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    # Create the analysis - it is missing the required "filename" key
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "details": json.dumps({"sandbox_url": "http://url.to.sandbox.report"}),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


def test_create_invalid_user_analysis(client, db):
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="User Analysis", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    # Create the analysis - it is missing the required "user_id" key
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "details": json.dumps({"username": "goodguy", "email": "goodguy@company.com"}),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("child_observables", []),
        ("child_observables", [{"type": "ipv4", "value": "192.168.1.1"}]),
        (
            "child_observables",
            [{"type": "ipv4", "value": "192.168.1.1"}, {"type": "fqdn", "value": "localhost.localdomain"}],
        ),
        ("details", None),
        ("details", "{}"),
        ("details", '{"foo": "bar"}'),
        ("error_message", None),
        ("error_message", "test"),
        ("stack_trace", None),
        ("stack_trace", "test"),
        ("summary", None),
        ("summary", "test"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client, db, key, value):
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test_type", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )
    factory.observable_type.create_or_read(value="ipv4", db=db)

    # Create the object
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
            key: value,
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details" and value:
        assert get.json()[key] == json.loads(value)
    # If the test is for child_observables, make sure the length is the same as the supplied list
    elif key == "child_observables":
        assert len(get.json()[key]) == len(value)
    else:
        assert get.json()[key] == value


def test_create_valid_required_fields(client, db):
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test_type", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    # Create the object
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back, but since there are no required fields to create the analysis, there is nothing to verify.
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200


def test_cached_analysis(client, db):
    # Create the first alert and add the analysis to it.
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test_type", version="1.0.0", db=db)
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    # Create the analysis
    create1 = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
        },
    )
    assert create1.status_code == status.HTTP_201_CREATED

    # Create a second alert with the same observable and analysis type. This should be cached.
    alert2 = factory.alert.create(db=db)

    # Create the analysis
    create2 = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert2.uuid),
            "target_uuid": str(observable.uuid),
        },
    )
    assert create2.status_code == status.HTTP_201_CREATED

    # The Content-Location headers should be the same from the two create API calls, which
    # indicates that the existing/cached analysis was used for the second API call.
    assert create1.headers["Content-Location"] == create2.headers["Content-Location"]


def test_expired_cached_analysis(client, db):
    # Create the first alert and add the analysis to it.
    alert = factory.alert.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(
        value="test_type", version="1.0.0", cache_seconds=0, db=db
    )
    observable = factory.observable.create_or_read(
        type="fqdn", value="localhost", parent_analysis=alert.root_analysis, db=db
    )

    # Create the analysis
    create1 = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert.uuid),
            "target_uuid": str(observable.uuid),
        },
    )
    assert create1.status_code == status.HTTP_201_CREATED

    # Create a second alert with the same observable and analysis type. The cache is expired since the analysis
    # module type's cache_seconds was set to 0.
    alert2 = factory.alert.create(db=db)

    # Create the analysis
    create2 = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "run_time": str(crud.helpers.utcnow()),
            "submission_uuid": str(alert2.uuid),
            "target_uuid": str(observable.uuid),
        },
    )
    assert create2.status_code == status.HTTP_201_CREATED

    # The Content-Location headers NOT should be the same from the two create API calls, which
    # indicates that the existing/cached analysis was expired and a new one was created.
    assert create1.headers["Content-Location"] != create2.headers["Content-Location"]
