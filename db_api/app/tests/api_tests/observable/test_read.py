import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/observable/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/observable/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get(client, db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=submission.root_analysis, db=db
    )

    get = client.get(f"/api/observable/{observable.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["object_type"] == "observable"


def test_get_all(client, db):
    # submission
    #  o1
    #  o2
    #    a
    #      o2

    submission = factory.submission.create(db=db)
    factory.observable.create_or_read(type="test_type", value="test", parent_analysis=submission.root_analysis, db=db)
    obs2 = factory.observable.create_or_read(
        type="test_type", value="test2", parent_analysis=submission.root_analysis, db=db
    )
    analysis = factory.analysis.create_or_read(
        analysis_module_type=factory.analysis_module_type.create_or_read(value="test_type", db=db),
        submission=submission,
        target=obs2,
        db=db,
    )
    # Adding a third observable somewhere in the submission tree with the same type+value combination is allowed,
    # but it will not result in a third entry in the observable table.
    factory.observable.create_or_read(type="test_type", value="test2", parent_analysis=analysis, db=db)

    # Read them back
    get = client.get("/api/observable/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 2


def test_get_all_empty(client):
    get = client.get("/api/observable/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 0


def test_observable_relationships(client, db):
    # submission
    #   o1
    #   o2
    #   o3 - IS_HASH_OF o1, IS_EQUAL_TO o2, BLAH analysis

    submission = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=submission.root_analysis, db=db
    )
    obs2 = factory.observable.create_or_read(
        type="test_type", value="test_value2", parent_analysis=submission.root_analysis, db=db
    )
    obs3 = factory.observable.create_or_read(
        type="test_type", value="test_value3", parent_analysis=submission.root_analysis, db=db
    )
    factory.observable_relationship.create_or_read(observable=obs3, related_observable=obs1, type="IS_HASH_OF", db=db)
    factory.observable_relationship.create_or_read(observable=obs3, related_observable=obs2, type="IS_EQUAL_TO", db=db)

    # The observable relationships should be sorted by the related observable's type then value.
    get = client.get(f"/api/observable/{obs3.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert len(obs3.relationships) == 2
    assert len(get.json()["observable_relationships"]) == 2
    assert get.json()["observable_relationships"][0]["type"]["value"] == "IS_HASH_OF"
    assert get.json()["observable_relationships"][0]["related_observable"]["uuid"] == str(obs1.uuid)
    assert get.json()["observable_relationships"][1]["type"]["value"] == "IS_EQUAL_TO"
    assert get.json()["observable_relationships"][1]["related_observable"]["uuid"] == str(obs2.uuid)
