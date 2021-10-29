from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from api.models.user_role import UserRoleCreate, UserRoleRead, UserRoleUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.user_role import UserRole


router = APIRouter(
    prefix="/user/role",
    tags=["User Role"],
)


#
# CREATE
#


def create_user_role(
    user_role: UserRoleCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    uuid = crud.create(obj=user_role, db_table=UserRole, db=db)

    response.headers["Content-Location"] = request.url_for("get_user_role", uuid=uuid)


helpers.api_route_create(router, create_user_role)


#
# READ
#


def get_all_user_roles(db: Session = Depends(get_db)):
    return crud.read_all(db_table=UserRole, db=db)


def get_user_role(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=UserRole, db=db)


helpers.api_route_read_all(router, get_all_user_roles, List[UserRoleRead])
helpers.api_route_read(router, get_user_role, UserRoleRead)


#
# UPDATE
#


def update_user_role(
    uuid: UUID,
    user_role: UserRoleUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    crud.update(uuid=uuid, obj=user_role, db_table=UserRole, db=db)

    response.headers["Content-Location"] = request.url_for("get_user_role", uuid=uuid)


helpers.api_route_update(router, update_user_role)


#
# DELETE
#


def delete_user_role(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=UserRole, db=db)


helpers.api_route_delete(router, delete_user_role)
