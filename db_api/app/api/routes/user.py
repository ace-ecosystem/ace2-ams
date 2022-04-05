from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from typing import Optional
from uuid import UUID

from api_models.auth import ValidateRefreshToken
from api_models.history import UserHistoryRead
from api_models.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)
from api.routes import helpers
from core.auth import hash_password
from db import crud
from db.database import get_db
from db.schemas.queue import Queue
from db.schemas.user import User, UserHistory
from db.schemas.user_role import UserRole


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
    # Create the new user using the data from the request
    new_user = User(**user.dict())

    # Get the queues from the database to associate with the new user
    new_user.default_alert_queue = crud.read_by_value(user.default_alert_queue, db_table=Queue, db=db)
    new_user.default_event_queue = crud.read_by_value(user.default_event_queue, db_table=Queue, db=db)

    # Get the user roles from the database to associate with the new user
    new_user.roles = crud.read_by_values(user.roles, db_table=UserRole, db=db)

    # Securely hash and salt the password. Bcrypt_256 is used to get around the Bcrypt limitations
    # of silently truncating passwords longer than 72 characters as well as not handling NULL bytes.
    new_user.password = hash_password(new_user.password)

    # Save the new user to the database
    db.add(new_user)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_user", uuid=new_user.uuid)


helpers.api_route_create(router, create_user)


#
# READ
#


def _join_as_subquery(query: select, subquery: select):
    s = subquery.subquery()
    return query.join(s, User.uuid == s.c.uuid).group_by(User.uuid)


def get_all_users(db: Session = Depends(get_db), enabled: Optional[bool] = None, username: Optional[str] = None):
    query = select(User).order_by(User.username)

    if enabled is not None:
        enabled_query = select(User).where(User.enabled == enabled)
        query = _join_as_subquery(query, enabled_query)

    if username:
        username_query = select(User).where(User.username == username)
        query = _join_as_subquery(query, username_query)

    return paginate(db, query)


def get_user(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=User, db=db)


def get_user_history(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read_history_records(history_table=UserHistory, record_uuid=uuid, db=db)


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
    # Read the current user from the database
    db_user: User = crud.read(uuid=uuid, db_table=User, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = user.dict(exclude_unset=True)

    # Keep track of all the diffs that were made
    diffs: list[crud.Diff] = []

    if "default_alert_queue" in update_data:
        diffs.append(
            crud.create_diff(
                field="default_alert_queue",
                old=db_user.default_alert_queue.value,
                new=update_data["default_alert_queue"],
            )
        )

        db_user.default_alert_queue = crud.read_by_value(
            value=update_data["default_alert_queue"], db_table=Queue, db=db
        )

    if "default_event_queue" in update_data:
        diffs.append(
            crud.create_diff(
                field="default_event_queue",
                old=db_user.default_event_queue.value,
                new=update_data["default_event_queue"],
            )
        )

        db_user.default_event_queue = crud.read_by_value(
            value=update_data["default_event_queue"], db_table=Queue, db=db
        )

    if "display_name" in update_data:
        diffs.append(crud.create_diff(field="display_name", old=db_user.display_name, new=update_data["display_name"]))
        db_user.display_name = update_data["display_name"]

    if "email" in update_data:
        diffs.append(crud.create_diff(field="email", old=db_user.email, new=update_data["email"]))
        db_user.email = update_data["email"]

    if "enabled" in update_data:
        diffs.append(crud.create_diff(field="enabled", old=db_user.enabled, new=update_data["enabled"]))
        db_user.enabled = update_data["enabled"]

    if "password" in update_data:
        diffs.append(crud.create_diff(field="password", old=None, new=None))
        db_user.password = hash_password(update_data["password"])

    if "roles" in update_data:
        diffs.append(crud.create_diff(field="roles", old=[x.value for x in db_user.roles], new=update_data["roles"]))
        db_user.roles = crud.read_by_values(values=update_data["roles"], db_table=UserRole, db=db)

    if "timezone" in update_data:
        diffs.append(crud.create_diff(field="timezone", old=db_user.timezone, new=update_data["timezone"]))
        db_user.timezone = update_data["timezone"]

    if "training" in update_data:
        diffs.append(crud.create_diff(field="training", old=db_user.training, new=update_data["training"]))
        db_user.training = update_data["training"]

    if "username" in update_data:
        diffs.append(crud.create_diff(field="username", old=db_user.username, new=update_data["username"]))
        db_user.username = update_data["username"]

    crud.commit(db)

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
    user: User = (
        db.execute(select(User).where(User.username == data.username, User.enabled == True)).scalars().one_or_none()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check the refresh token against the database to ensure it is valid. If the token does not match, it may mean
    # that someone is trying to use an old refresh token. In this case, remove the current refresh token from the
    # database to require the user to fully log in again.
    if data.refresh_token != user.refresh_token:
        user.refresh_token = None
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Reused token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Rotate the refresh token and save it to the database
    user.refresh_token = data.new_refresh_token
    db.commit()

    return user


helpers.api_route_auth(
    router,
    validate_refresh_token,
    path="/validate_refresh_token",
    response_model=UserRead,
    success_desc="Token is valid",
    failure_desc="Token is invalid",
)
