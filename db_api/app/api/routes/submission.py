from datetime import datetime
from api_models.summaries import URLDomainSummary
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api.routes import helpers
from api_models.create import Create
from api_models.history import SubmissionHistoryRead
from api_models.observable import ObservableSubmissionRead
from api_models.submission import SubmissionCreate, SubmissionRead, SubmissionUpdate
from db import crud
from db.database import get_db
from db.schemas.submission import SubmissionHistory
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase, VersionMismatch


router = APIRouter(
    prefix="/submission",
    tags=["Submission"],
)


#
# CREATE
#


def create_submission(
    submission: SubmissionCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        submission = crud.submission.create_or_read(model=submission, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_submission", uuid=submission.uuid)

    return {"uuid": submission.uuid}


helpers.api_route_create(router, create_submission, response_model=Create)


#
# READ
#


def get_all_submissions(
    db: Session = Depends(get_db),
    alert: Optional[bool] = None,
    disposition: Optional[list[str]] = Query(None),
    not_disposition: Optional[list[str]] = Query(None),
    disposition_user: Optional[list[str]] = Query(None),
    not_disposition_user: Optional[list[str]] = Query(None),
    dispositioned_after: Optional[list[datetime]] = Query(None),
    dispositioned_before: Optional[list[datetime]] = Query(None),
    event_uuid: Optional[list[UUID]] = Query(None),
    event_time_after: Optional[list[datetime]] = Query(None),
    event_time_before: Optional[list[datetime]] = Query(None),
    insert_time_after: Optional[list[datetime]] = Query(None),
    insert_time_before: Optional[list[datetime]] = Query(None),
    name: Optional[list[str]] = Query(None),
    observable: Optional[list[str]] = Query(None, regex="^[\w\-]+\|.+$"),  # type|value
    observable_types: Optional[list[str]] = Query(None),
    observable_value: Optional[list[str]] = Query(None),
    owner: Optional[list[str]] = Query(None),
    queue: Optional[list[str]] = Query(None),
    sort: Optional[str] = Query(
        None,
        regex=""
        "^("
        "(disposition)|"
        "(disposition_time)|"
        "(disposition_user)|"
        "(event_time)|"
        "(insert_time)|"
        "(name)|"
        "(owner)|"
        "(queue)|"
        "(submission_type)"
        ")\|"
        "("
        "(asc)|"
        "(desc)"
        ")$",
    ),  # Example: event_time|desc,
    submission_type: Optional[list[str]] = Query(None),
    tags: Optional[list[str]] = Query(None),
    threat_actors: Optional[list[str]] = Query(None),
    threats: Optional[list[str]] = Query(None),
    tool: Optional[list[str]] = Query(None),
    tool_instance: Optional[list[str]] = Query(None),
):
    return paginate(
        conn=db,
        query=crud.submission.build_read_all_query(
            alert=alert,
            disposition=disposition,
            not_disposition=not_disposition,
            disposition_user=disposition_user,
            not_disposition_user=not_disposition_user,
            dispositioned_after=dispositioned_after,
            dispositioned_before=dispositioned_before,
            event_uuid=event_uuid,
            event_time_after=event_time_after,
            event_time_before=event_time_before,
            insert_time_after=insert_time_after,
            insert_time_before=insert_time_before,
            name=name,
            observable=observable,
            observable_types=observable_types,
            observable_value=observable_value,
            owner=owner,
            queue=queue,
            sort=sort,
            submission_type=submission_type,
            tags=tags,
            threat_actors=threat_actors,
            threats=threats,
            tool=tool,
            tool_instance=tool_instance,
        ),
    )


def get_submission(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.submission.read_tree(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Submission {uuid} does not exist") from e


def get_submission_history(uuid: UUID, db: Session = Depends(get_db)):
    return paginate(
        conn=db, query=crud.history.build_read_history_query(history_table=SubmissionHistory, record_uuid=uuid)
    )


def get_submissions_observables(uuids: list[UUID], db: Session = Depends(get_db)):
    return crud.submission.read_observables(uuids=uuids, db=db)


def get_url_domain_summary(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.submission.read_summary_url_domain(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Submission {uuid} does not exist") from e


helpers.api_route_read_all(router, get_all_submissions, SubmissionRead)
helpers.api_route_read(router, get_submission, dict)
helpers.api_route_read_all(router, get_submission_history, SubmissionHistoryRead, path="/{uuid}/history")
helpers.api_route_read(
    router, get_submissions_observables, list[ObservableSubmissionRead], methods=["POST"], path="/observables"
)
helpers.api_route_read(router, get_url_domain_summary, URLDomainSummary, path="/{uuid}/summary/url_domain")


#
# UPDATE
#


def update_submissions(
    submissions: list[SubmissionUpdate],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    for submission in submissions:
        try:
            crud.submission.update(model=submission, db=db)
        except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except VersionMismatch as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

        response.headers["Content-Location"] = request.url_for("get_submission", uuid=submission.uuid)

    db.commit()


helpers.api_route_update(router, update_submissions, path="/")
