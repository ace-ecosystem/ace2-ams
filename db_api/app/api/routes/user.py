from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api.routes import helpers
from api_models.auth import ValidateRefreshToken
from api_models.history import UserHistoryRead
from api_models.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)
from db import crud
from db.database import get_db
from db.schemas.user import UserHistory
from exceptions.db import ReusedToken, UserIsDisabled, UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


#
# CREATE
#


def create_user(
    user: UserCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        obj = crud.user.create_or_read(model=user, db=db)
    except ValueNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_user", uuid=obj.uuid)


helpers.api_route_create(router, create_user)


#
# READ
#


def get_all_users(db: Session = Depends(get_db), enabled: Optional[bool] = None, username: Optional[str] = None):
    return paginate(
        conn=db,
        query=crud.user.build_read_all_query(enabled=enabled, username=username),
    )


def get_user(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.user.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {uuid} does not exist") from e


def get_user_history(uuid: UUID, db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.history.build_read_history_query(history_table=UserHistory, record_uuid=uuid))


helpers.api_route_read_all(router, get_all_users, UserRead)
helpers.api_route_read(router, get_user, UserRead)
helpers.api_route_read_all(router, get_user_history, UserHistoryRead, path="/{uuid}/history")


#
# UPDATE
#


def update_user(
    uuid: UUID,
    user: UserUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.user.update(uuid=uuid, model=user, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update user {uuid}")
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_user", uuid=uuid)


helpers.api_route_update(router, update_user)


#
# DELETE
#


# Deleting users is not currently supported (mark them as disabled instead)


#
# VALIDATE REFRESH TOKEN
#


def validate_refresh_token(
    data: ValidateRefreshToken,
    db: Session = Depends(get_db),
):
    try:
        return crud.user.validate_refresh_token(data=data, db=db)
    except ReusedToken as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Reused token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except UserIsDisabled as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except ValueNotFoundInDatabase as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


helpers.api_route_auth(
    router,
    validate_refresh_token,
    path="/validate_refresh_token",
    response_model=UserRead,
    success_desc="Token is valid",
    failure_desc="Token is invalid",
)
