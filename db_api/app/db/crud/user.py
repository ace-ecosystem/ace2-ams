import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from typing import Optional
from uuid import UUID
from api_models.auth import Auth, ValidateRefreshToken

from api_models.user import UserCreate, UserUpdate
from core.auth import hash_password, verify_password
from db import crud
from db.schemas.user import User, UserHistory
from exceptions.db import ReusedToken, UserIsDisabled, ValueNotFoundInDatabase


def auth(auth: Auth, db: Session) -> User:
    user = read_by_username(username=auth.username, db=db)

    if not user.enabled or not verify_password(auth.password, user.password):
        raise ValueError("Invalid username or password")

    # Save the new refresh token to the database
    user.refresh_token = auth.new_refresh_token
    db.flush()

    return user


def build_read_all_query(
    enabled: Optional[bool] = None,
    username: Optional[str] = None,
) -> Select:
    def _join_as_subquery(query: Select, subquery: Select):
        s = subquery.subquery()
        return query.join(s, User.uuid == s.c.uuid).group_by(User.uuid)

    query = select(User).order_by(User.username)

    if enabled is not None:
        enabled_query = select(User).where(User.enabled == enabled)
        query = _join_as_subquery(query, enabled_query)

    if username:
        username_query = select(User).where(User.username == username)
        query = _join_as_subquery(query, username_query)

    return query


def create_or_read(model: UserCreate, db: Session) -> User:
    obj = User(
        default_alert_queue=crud.queue.read_by_value(value=model.default_alert_queue, db=db),
        default_event_queue=crud.queue.read_by_value(value=model.default_event_queue, db=db),
        display_name=model.display_name,
        email=model.email,
        enabled=model.enabled,
        password=hash_password(model.password),
        roles=crud.user_role.read_by_values(values=model.roles, db=db),
        timezone=model.timezone,
        training=model.training,
        username=model.username,
        uuid=model.uuid,
    )

    # If the user could not be created, that implies the user already exists, so return that one instead.
    if not crud.helpers.create(obj=obj, db=db):
        return read_by_username(username=model.username, db=db)

    # Add a user history entry if the history username was given.
    if model.history_username is not None:
        crud.history.record_create_history(
            history_table=UserHistory,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            record=obj,
            db=db,
        )

    return obj


def read_by_username(username: Optional[str], db: Session) -> User:
    try:
        return db.execute(select(User).where(User.username == username)).scalars().one()
    except NoResultFound as e:
        raise ValueNotFoundInDatabase(f"The '{username}' user was not found in the user table.") from e


def read_by_uuid(uuid: UUID, db: Session) -> User:
    return crud.helpers.read_by_uuid(db_table=User, uuid=uuid, db=db)


def update(uuid: UUID, model: UserUpdate, db: Session) -> bool:
    with db.begin_nested():
        # Read the current user from the database
        user = read_by_uuid(uuid=uuid, db=db)

        # Get the data that was given in the request and use it to update the database object
        update_data = model.dict(exclude_unset=True)

        # Keep track of all the diffs that were made
        diffs: list[crud.history.Diff] = []

        if "default_alert_queue" in update_data:
            diffs.append(
                crud.history.create_diff(
                    field="default_alert_queue",
                    old=user.default_alert_queue.value,
                    new=update_data["default_alert_queue"],
                )
            )

            user.default_alert_queue = crud.queue.read_by_value(value=update_data["default_alert_queue"], db=db)

        if "default_event_queue" in update_data:
            diffs.append(
                crud.history.create_diff(
                    field="default_event_queue",
                    old=user.default_event_queue.value,
                    new=update_data["default_event_queue"],
                )
            )

            user.default_event_queue = crud.queue.read_by_value(value=update_data["default_event_queue"], db=db)

        if "display_name" in update_data:
            diffs.append(
                crud.history.create_diff(field="display_name", old=user.display_name, new=update_data["display_name"])
            )
            user.display_name = update_data["display_name"]

        if "email" in update_data:
            diffs.append(crud.history.create_diff(field="email", old=user.email, new=update_data["email"]))
            user.email = update_data["email"]

        if "enabled" in update_data:
            diffs.append(crud.history.create_diff(field="enabled", old=user.enabled, new=update_data["enabled"]))
            user.enabled = update_data["enabled"]

        if "password" in update_data:
            diffs.append(crud.history.create_diff(field="password", old=None, new=None))
            user.password = hash_password(update_data["password"])

        if "roles" in update_data:
            diffs.append(
                crud.history.create_diff(field="roles", old=[x.value for x in user.roles], new=update_data["roles"])
            )
            user.roles = crud.user_role.read_by_values(values=update_data["roles"], db=db)

        if "timezone" in update_data:
            diffs.append(crud.history.create_diff(field="timezone", old=user.timezone, new=update_data["timezone"]))
            user.timezone = update_data["timezone"]

        if "training" in update_data:
            diffs.append(crud.history.create_diff(field="training", old=user.training, new=update_data["training"]))
            user.training = update_data["training"]

        if "username" in update_data:
            diffs.append(crud.history.create_diff(field="username", old=user.username, new=update_data["username"]))
            user.username = update_data["username"]

        # Try to flush the changes to the database
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            return False

    # Add a user history entry if the history username was given.
    if model.history_username:
        crud.history.record_update_history(
            history_table=UserHistory,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            record=user,
            diffs=diffs,
            db=db,
        )

    return True


def validate_refresh_token(data: ValidateRefreshToken, db: Session) -> User:
    user = read_by_username(username=data.username, db=db)
    if not user.enabled:
        raise UserIsDisabled(f"User {data.username} is disabled")

    # Check the refresh token against the database to ensure it is valid. If the token does not match, it may mean
    # that someone is trying to use an old refresh token. In this case, remove the current refresh token from the
    # database to require the user to fully log in again.
    if data.refresh_token != user.refresh_token:
        logging.critical(f"!!!!! db token = {user.refresh_token}")
        logging.critical(f"!!!!! token = {data.refresh_token}")
        user.refresh_token = None
        db.commit()
        raise ReusedToken("Detected a potentially reused token")

    # Rotate the refresh token and save it to the database
    user.refresh_token = data.new_refresh_token
    db.commit()

    return user
