import pytest

from db import crud
from exceptions.db import ValueNotFoundInDatabase
from tests import factory


#
# INVALID TESTS
#


def test_read_nonexistent(db):
    submission = factory.submission.create(db=db)

    factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", db=db
    )

    with pytest.raises(ValueNotFoundInDatabase):
        crud.analysis_summary_detail.read_by_analysis_header_content(
            analysis_uuid=submission.root_analysis_uuid, header="test2", content="test2", db=db
        )


#
# VALID TESTS
#


def test_read_by_uuid(db):
    submission = factory.submission.create(db=db)

    obj = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", db=db
    )

    result = crud.analysis_summary_detail.read_by_uuid(uuid=obj.uuid, db=db)
    assert result.uuid == obj.uuid


def test_read_by_value(db):
    submission = factory.submission.create(db=db)

    obj = factory.analysis_summary_detail.create_or_read(
        analysis=submission.root_analysis, header="test", content="test", db=db
    )

    result = crud.analysis_summary_detail.read_by_analysis_header_content(
        analysis_uuid=submission.root_analysis_uuid, header="test", content="test", db=db
    )
    assert result.uuid == obj.uuid
