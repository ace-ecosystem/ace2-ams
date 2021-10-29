from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import delete as sql_delete, select, update as sql_update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Optional, Union
from uuid import UUID

from core.auth import verify_password
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType
from db.schemas.user import User


#
# AUTH
#


def auth(username: str, password: str, db: Session) -> Optional[User]:
    """Returns the user from the database if the given username and password are valid."""

    user = db.execute(select(User).where(User.username == username)).scalars().one_or_none()

    if user and verify_password(password, user.password):
        return user

    return None


#
# CREATE
#


def create(obj: BaseModel, db_table: DeclarativeMeta, db: Session) -> UUID:
    """Creates a new object in the given database table. Returns the new object's UUID.
    Designed to be called only by the API since it raises an HTTPException."""

    new_obj = db_table(**obj.dict())
    db.add(new_obj)
    commit(db)
    return new_obj.uuid


#
# READ
#


def read_all(db_table: DeclarativeMeta, db: Session) -> List:
    """Returns all objects from the given database table."""

    return db.execute(select(db_table)).scalars().all()


def read(uuid: UUID, db_table: DeclarativeMeta, db: Session):
    """Returns the single object with the given UUID if it exists, otherwise returns None.
    Designed to be called only by the API since it raises an HTTPException."""

    result = db.execute(select(db_table).where(db_table.uuid == uuid)).scalars().one_or_none()

    if result is None:
        raise HTTPException(status_code=404, detail=f"UUID {uuid} does not exist.")

    return result


def read_by_uuids(uuids: List[UUID], db_table: DeclarativeMeta, db: Session):
    """Returns a list of objects with the given UUIDs. Designed to be called only by the API
    since it raises an HTTPException."""

    # Return without performing a database query if the list of values is empty
    if uuids == []:
        return uuids

    # Only search the database for unique UUIDs
    uuids = list(set(uuids))

    resources = db.execute(select(db_table).where(db_table.uuid.in_(uuids))).scalars().all()

    for uuid in uuids:
        if not any(uuid == r.uuid for r in resources):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The {uuid} {db_table} does not exist",
            )

    return resources


def read_observable(type: str, value: str, db: Session) -> Union[Observable, None]:
    """Returns the Observable with the given type and value if it exists."""

    return (
        db.execute(
            select(Observable).join(ObservableType).where(ObservableType.value == type, Observable.value == value)
        )
        .scalars()
        .one_or_none()
    )


def read_user_by_username(username: str, db: Session) -> User:
    """Returns the User with the given username if it exists. Designed to be called only
    by the API since it raises an HTTPException."""

    try:
        return db.execute(select(User).where(User.username == username)).scalars().one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user {username} does not exist",
        )


def read_by_value(value: str, db_table: DeclarativeMeta, db: Session):
    """Returns an object from the given database table with the given value.
    Designed to be called only by the API since it raises an HTTPException."""

    # Return early if the value is None
    if not value:
        return None

    try:
        return db.execute(select(db_table).where(db_table.value == value)).scalars().one()
    # MultipleResultsFound exception is not caught since each database table that has a
    # value column should be configured to have that column be unique.
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The {value} {db_table} does not exist",
        )


def read_by_values(values: List[str], db_table: DeclarativeMeta, db: Session):
    """Returns a list of objects from the given database table with the given values.
    Designed to be called only by the API since it raises an HTTPException."""

    # Return without performing a database query if the list of values is empty or None
    if not values:
        return []

    # Only search the database for unique values
    values = list(set(values))

    resources = db.execute(select(db_table).where(db_table.value.in_(values))).scalars().all()

    for value in values:
        if not any(value == r.value for r in resources):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The {value} {db_table} does not exist",
            )

    return resources


#
# UPDATE
#


def update(uuid: UUID, obj: BaseModel, db_table: DeclarativeMeta, db: Session):
    """Updates the object with the given UUID in the database.
    Designed to be called only by the API since it raises an HTTPException."""

    # Try to perform the update
    try:
        result = db.execute(
            sql_update(db_table)
            .where(db_table.uuid == uuid)
            .values(
                # exclude_unset is needed for update routes so that any values in the Pydantic model
                # that are not being updated are not set to None. Instead they will be removed from the dict.
                **obj.dict(exclude_unset=True)
            )
        )

        # Verify a row was actually updated
        if result.rowcount != 1:
            raise HTTPException(status_code=404, detail=f"UUID {uuid} does not exist.")

        commit(db)

    # An IntegrityError will happen if value already exists or was set to None
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Got an IntegrityError while updating UUID {uuid}.",
        )


#
# DELETE
#


def delete(uuid: UUID, db_table: DeclarativeMeta, db: Session):
    """Deletes the object with the given UUID from the database.
    Designed to be called only by the API since it raises an HTTPException."""

    # Make sure the resource exists so that better error messages can be returned. The read
    # function will raise an exception and return a 404 status if the resource does not exist.
    result = read(uuid=uuid, db_table=db_table, db=db)

    # NOTE: This will need to be updated to account for foreign key constraint errors.
    result = db.execute(sql_delete(db_table).where(db_table.uuid == uuid))

    # If the rowcount is not 1, it means the resource could not be deleted. Because we know at
    # this point that the resource actually exists, it could not be deleted due to a foreign
    # key constraint.
    if result.rowcount != 1:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to delete {db_table} UUID {uuid} due to a foreign key constraint.",
        )

    commit(db)


#
# COMMIT
#


def commit(db: Session):
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Got an IntegrityError while committing the database session: {e}",
        )
