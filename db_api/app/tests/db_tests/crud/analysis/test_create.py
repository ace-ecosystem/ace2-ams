import json
import pytest

from datetime import datetime, timedelta
from uuid import uuid4

from api_models.analysis import AnalysisCreate
from db import crud
from exceptions.db import UuidNotFoundInDatabase
from tests import factory


#
# INVALID TESTS
#


def test_create_nonexistent_analysis_module_type(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test", value="test", parent_analysis=submission.root_analysis, db=db
    )

    with pytest.raises(UuidNotFoundInDatabase):
        crud.analysis.create_or_read(
            model=AnalysisCreate(
                analysis_module_type_uuid=uuid4(), submission_uuid=submission.uuid, target_uuid=observable.uuid
            ),
            db=db,
        )


def test_create_nonexistent_submission(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test", value="test", parent_analysis=submission.root_analysis, db=db
    )
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", db=db)

    with pytest.raises(UuidNotFoundInDatabase):
        crud.analysis.create_or_read(
            model=AnalysisCreate(
                analysis_module_type_uuid=analysis_module_type.uuid,
                submission_uuid=uuid4(),
                target_uuid=observable.uuid,
            ),
            db=db,
        )


def test_create_nonexistent_target(db):
    submission = factory.submission.create(db=db)
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", db=db)

    with pytest.raises(UuidNotFoundInDatabase):
        crud.analysis.create_or_read(
            model=AnalysisCreate(
                analysis_module_type_uuid=analysis_module_type.uuid,
                submission_uuid=submission.uuid,
                target_uuid=uuid4(),
            ),
            db=db,
        )


#
# VALID TESTS
#


def test_create(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test", value="test", parent_analysis=submission.root_analysis, db=db
    )
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", cache_seconds=90, db=db)
    factory.observable_type.create_or_read(value="ipv4", db=db)

    # Create the analysis
    now = crud.helpers.utcnow()
    analysis = crud.analysis.create_or_read(
        model=AnalysisCreate(
            analysis_module_type_uuid=analysis_module_type.uuid,
            child_observables=[{"type": "ipv4", "value": "192.168.1.1"}],
            details=json.dumps({}),
            error_message="test error",
            run_time=now,
            stack_trace="test stack trace",
            submission_uuid=submission.uuid,
            summary="test summary",
            target_uuid=observable.uuid,
        ),
        db=db,
    )

    assert analysis.analysis_module_type == analysis_module_type
    assert analysis.cached_until == now + timedelta(seconds=analysis_module_type.cache_seconds)
    assert analysis.child_observables[0].value == "192.168.1.1"
    assert analysis.details == {}
    assert analysis.error_message == "test error"
    assert analysis.run_time == now
    assert analysis.stack_trace == "test stack trace"
    assert analysis.summary == "test summary"
    assert analysis.target == observable


def test_cached_analysis(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test", value="test", parent_analysis=submission.root_analysis, db=db
    )
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", cache_seconds=90, db=db)

    # Create the first analysis
    analysis = crud.analysis.create_or_read(
        model=AnalysisCreate(
            analysis_module_type_uuid=analysis_module_type.uuid,
            submission_uuid=submission.uuid,
            target_uuid=observable.uuid,
        ),
        db=db,
    )

    # Create a second analysis of the same type for the same target observable
    submission2 = factory.submission.create(db=db)
    analysis2 = crud.analysis.create_or_read(
        model=AnalysisCreate(
            analysis_module_type_uuid=analysis_module_type.uuid,
            submission_uuid=submission2.uuid,
            target_uuid=observable.uuid,
        ),
        db=db,
    )

    # The second analysis should be the cached version of the first analysis
    assert analysis2.uuid == analysis.uuid


def test_expired_cached_analysis(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test", value="test", parent_analysis=submission.root_analysis, db=db
    )
    # cache_seconds is set to 0 so that the analysis immediately expires from cache
    analysis_module_type = factory.analysis_module_type.create_or_read(value="test", cache_seconds=0, db=db)

    # Create the first analysis
    analysis = crud.analysis.create_or_read(
        model=AnalysisCreate(
            analysis_module_type_uuid=analysis_module_type.uuid,
            submission_uuid=submission.uuid,
            target_uuid=observable.uuid,
        ),
        db=db,
    )

    # Create a second analysis of the same type for the same target observable
    submission2 = factory.submission.create(db=db)
    analysis2 = crud.analysis.create_or_read(
        model=AnalysisCreate(
            analysis_module_type_uuid=analysis_module_type.uuid,
            submission_uuid=submission2.uuid,
            target_uuid=observable.uuid,
        ),
        db=db,
    )

    # The second analysis should be a unique analysis
    assert analysis2.uuid != analysis.uuid


def test_validate_email_analysis_details(db):
    analysis_module_type = factory.analysis_module_type.create_or_read(value="Email Analysis", db=db)

    crud.analysis.validate_analysis_details(
        analysis_module_type=analysis_module_type,
        details={
            "from_address": "badguy@evil.com",
            "headers": "blah",
            "message_id": "<abcd1234@evil.com>",
            "time": datetime.now().isoformat(),
            "to_address": "goodguy@company.com",
        },
    )


def test_validate_faqueue_analysis_details(db):
    analysis_module_type = factory.analysis_module_type.create_or_read(value="FA Queue Analysis", db=db)

    crud.analysis.validate_analysis_details(
        analysis_module_type=analysis_module_type,
        details={"hits": 0},
    )


def test_validate_sandbox_analysis_details(db):
    analysis_module_type = factory.analysis_module_type.create_or_read(value="Sandbox Analysis", db=db)

    crud.analysis.validate_analysis_details(
        analysis_module_type=analysis_module_type,
        details={"filename": "malware.exe", "sandbox_url": "http://localhost"},
    )


def test_validate_user_analysis_details(db):
    analysis_module_type = factory.analysis_module_type.create_or_read(value="User Analysis", db=db)

    crud.analysis.validate_analysis_details(
        analysis_module_type=analysis_module_type,
        details={"email": "goodguy@company.com", "user_id": "12345"},
    )
