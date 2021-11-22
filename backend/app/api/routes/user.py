from fastapi import APIRouter, Depends, Request, Response
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from uuid import UUID

from api.models.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)
from api.routes import helpers
from core.auth import hash_password
from db import crud
from db.database import get_db
from db.schemas.alert_queue import AlertQueue
from db.schemas.user import User
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

    # Get the alert queue from the database to associate with the new user
    new_user.default_alert_queue = crud.read_by_value(user.default_alert_queue, db_table=AlertQueue, db=db)

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


def get_all_users(db: Session = Depends(get_db)):
    return paginate(db, select(User))


def get_user(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=User, db=db)


helpers.api_route_read_all(router, get_all_users, UserRead)
helpers.api_route_read(router, get_user, UserRead)


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

    if "default_alert_queue" in update_data:
        db_user.default_alert_queue = crud.read_by_value(
            value=update_data["default_alert_queue"], db_table=AlertQueue, db=db
        )

    if "display_name" in update_data:
        db_user.display_name = update_data["display_name"]

    if "email" in update_data:
        db_user.email = update_data["email"]

    if "enabled" in update_data:
        db_user.enabled = update_data["enabled"]

    if "password" in update_data:
        db_user.password = hash_password(update_data["password"])

    if "roles" in update_data:
        db_user.roles = crud.read_by_values(values=update_data["roles"], db_table=UserRole, db=db)

    if "timezone" in update_data:
        db_user.timezone = update_data["timezone"]

    if "username" in update_data:
        db_user.username = update_data["username"]

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_user", uuid=uuid)


helpers.api_route_update(router, update_user)


#
# DELETE
#


def delete_user(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=User, db=db)


helpers.api_route_delete(router, delete_user)
