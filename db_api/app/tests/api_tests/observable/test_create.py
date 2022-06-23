import pytest
import uuid

from fastapi import status

from db.schemas.observable import Observable
from tests.api_tests.node import INVALID_LIST_STRING_VALUES, VALID_LIST_STRING_VALUES
from tests import factory


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("context", 123),
        ("context", ""),
        ("expires_on", ""),
        ("expires_on", "Monday"),
        ("expires_on", "2022-01-01"),
        ("for_detection", 123),
        ("for_detection", None),
        ("for_detection", "True"),
        ("parent_analysis_uuid", 123),
        ("parent_analysis_uuid", ""),
        ("parent_analysis_uuid", "abc"),
        ("type", 123),
        ("type", None),
        ("type", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("uuid", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {"type": "test_type", "value": "test", key: value}
    create = client.post("/api/observable/", json=[create_json])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(create.json()["detail"]) == 1
    assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key,values",
    [
        ("tags", INVALID_LIST_STRING_VALUES),
        ("threat_actors", INVALID_LIST_STRING_VALUES),
        ("threats", INVALID_LIST_STRING_VALUES),
    ],
)
def test_create_invalid_node_fields(client, db, key, values):
    submission = factory.submission.create(db=db)
    for value in values:
        create = client.post(
            "/api/observable/",
            json=[
                {
                    key: value,
                    "type": "test_type",
                    "value": "test",
                    "parent_analysis_uuid": str(submission.root_analysis_uuid),
                }
            ],
        )
        assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key",
    [
        ("type"),
        ("value"),
    ],
)
def test_create_missing_required_fields(client, db, key):
    submission = factory.submission.create(db=db)
    create_json = {"type": "test_type", "value": "test", "parent_analysis_uuid": str(submission.root_analysis_uuid)}
    del create_json[key]
    create = client.post("/api/observable/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_parent_analysis(client, db):
    factory.observable_type.create_or_read(value="test_type", db=db)

    nonexistent_uuid = str(uuid.uuid4())
    create = client.post(
        "/api/observable/",
        json=[{"parent_analysis_uuid": nonexistent_uuid, "type": "test_type", "value": "test"}],
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert nonexistent_uuid in create.text


@pytest.mark.parametrize(
    "key",
    [("tags"), ("threat_actors"), ("threats")],
)
def test_create_nonexistent_node_fields(client, db, key):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test_type", db=db)

    create = client.post(
        "/api/observable/",
        json=[
            {
                key: ["abc"],
                "type": "test_type",
                "value": "test",
                "parent_analysis_uuid": str(submission.root_analysis_uuid),
            }
        ],
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in create.text


def test_create_nonexistent_type(client, db):
    submission = factory.submission.create(db=db)
    nonexistent_type = "test_type"
    create = client.post(
        "/api/observable/",
        json=[{"type": nonexistent_type, "value": "test", "parent_analysis_uuid": str(submission.root_analysis_uuid)}],
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert nonexistent_type in create.text


#
# VALID TESTS
#


def test_get_version(client, db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=submission.root_analysis, db=db
    )

    get = client.get(f"/api/observable/{observable.uuid}/version")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == {"version": str(observable.version)}


def test_create_verify_history(client, db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test_type", db=db)

    # Create some observables
    observables = [
        {
            "uuid": str(uuid.uuid4()),
            "type": "test_type",
            "value": f"test{i}",
            "history_username": "analyst",
            "parent_analysis_uuid": str(submission.root_analysis_uuid),
        }
        for i in range(3)
    ]
    create = client.post("/api/observable/", json=observables)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history records
    for observable in observables:
        history = client.get(f"/api/observable/{observable['uuid']}/history")
        assert history.json()["total"] == 1
        assert history.json()["items"][0]["action"] == "CREATE"
        assert history.json()["items"][0]["action_by"]["username"] == "analyst"
        assert history.json()["items"][0]["record_uuid"] == observable["uuid"]
        assert history.json()["items"][0]["field"] is None
        assert history.json()["items"][0]["diff"] is None
        assert history.json()["items"][0]["snapshot"]["value"] == observable["value"]


def test_create_bulk(client, db):
    # Create an submission
    submission = factory.submission.create(db=db)
    initial_submission_version = submission.version

    # Create an observable type
    factory.observable_type.create_or_read(value="test_type", db=db)

    # Create some observables
    observables = [
        {"type": "test_type", "value": f"test{i}", "parent_analysis_uuid": str(submission.root_analysis_uuid)}
        for i in range(3)
    ]

    create = client.post("/api/observable/", json=observables)
    assert create.status_code == status.HTTP_201_CREATED

    # There should be 3 observables in the database
    observables = db.query(Observable).all()
    assert len(observables) == 3

    # Additionally, creating an observable should trigger the submission to get a new version.
    assert submission.version != initial_submission_version


@pytest.mark.parametrize(
    "key,value",
    [
        ("context", None),
        ("context", "test"),
        ("expires_on", None),
        ("expires_on", 1640995200),
        ("expires_on", "2022-01-01T00:00:00Z"),
        ("expires_on", "2022-01-01 00:00:00"),
        ("expires_on", "2022-01-01 00:00:00.000000"),
        ("expires_on", "2021-12-31 19:00:00-05:00"),
        ("for_detection", False),
        ("for_detection", True),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client, db, key, value):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test_type", db=db)

    # Create the object
    create = client.post(
        "/api/observable/",
        json=[
            {
                key: value,
                "type": "test_type",
                "value": "test",
                "parent_analysis_uuid": str(submission.root_analysis_uuid),
            }
        ],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if key == "expires_on" and value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == value


def test_create_valid_required_fields(client, db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test_type", db=db)

    # Create the object
    create = client.post(
        "/api/observable/",
        json=[{"type": "test_type", "value": "test", "parent_analysis_uuid": str(submission.root_analysis_uuid)}],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("tags", VALID_LIST_STRING_VALUES, factory.metadata_tag.create_or_read),
        ("threat_actors", VALID_LIST_STRING_VALUES, factory.threat_actor.create_or_read),
        ("threats", VALID_LIST_STRING_VALUES, factory.threat.create_or_read),
    ],
)
def test_create_valid_node_fields(client, db, key, value_lists, helper_create_func):
    submission = factory.submission.create(db=db)

    for value_list in value_lists:
        for value in value_list:
            helper_create_func(value=value, db=db)

        # Create an observable type
        factory.observable_type.create_or_read(value="test_type", db=db)

        create = client.post(
            "/api/observable/",
            json=[
                {
                    key: value_list,
                    "type": "test_type",
                    "value": f"{key}{value_list}",
                    "parent_analysis_uuid": str(submission.root_analysis_uuid),
                }
            ],
        )
        assert create.status_code == status.HTTP_201_CREATED

        # Read it back
        get = client.get(create.headers["Content-Location"])
        assert len(get.json()[key]) == len(list(set(value_list)))
