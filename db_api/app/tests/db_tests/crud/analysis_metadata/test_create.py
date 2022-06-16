from api_models.analysis_metadata import AnalysisMetadataCreate
from db import crud
from tests import factory


#
# TAG
#


def test_create_duplicate_tag(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )
    assert observable.all_analysis_metadata == []

    # Create the first tag
    analysis_metadata = crud.analysis_metadata.create_or_read(
        model=AnalysisMetadataCreate(
            analysis_uuid=submission.root_analysis_uuid,
            observable_uuid=observable.uuid,
            type="tag",
            value="metadata_tag",
        ),
        db=db,
    )
    assert observable.all_analysis_metadata == [analysis_metadata]

    # Try to create the same tag on the same observable. It should be the same object.
    analysis_metadata2 = crud.analysis_metadata.create_or_read(
        model=AnalysisMetadataCreate(
            analysis_uuid=submission.root_analysis_uuid,
            observable_uuid=observable.uuid,
            type="tag",
            value="metadata_tag",
        ),
        db=db,
    )
    assert analysis_metadata2 == analysis_metadata
    assert observable.all_analysis_metadata == [analysis_metadata]


def test_create_tag_with_uuids(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )

    assert observable.all_analysis_metadata == []

    analysis_metadata = crud.analysis_metadata.create_or_read(
        model=AnalysisMetadataCreate(
            analysis_uuid=submission.root_analysis_uuid,
            observable_uuid=observable.uuid,
            type="tag",
            value="metadata_tag",
        ),
        db=db,
    )

    assert observable.all_analysis_metadata == [analysis_metadata]
