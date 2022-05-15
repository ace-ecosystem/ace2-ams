from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.user_role import UserRoleCreate, UserRoleRead, UserRoleUpdate
from db import crud
from db.database import get_db
from db.schemas.user_role import UserRole
from exceptions.db import UuidNotFoundInDatabase


router = APIRouter(
    prefix="/user/role",
    tags=["User Role"],
)


#
# CREATE
#


def create_user_role(
    create: UserRoleCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    obj = crud.user_role.create_or_read(model=create, db=db)

    response.headers["Content-Location"] = request.url_for("get_user_role", uuid=obj.uuid)


helpers.api_route_create(router, create_user_role)


#
# READ
#


def get_all_user_roles(db: Session = Depends(get_db)):
    return paginate(conn=db, query=crud.helpers.build_read_all_query(UserRole).order_by(UserRole.value))


def get_user_role(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.user_role.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_read_all(router, get_all_user_roles, UserRoleRead)
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
    try:
        if not crud.helpers.update(uuid=uuid, update_model=user_role, db_table=UserRole, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to update user role {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    response.headers["Content-Location"] = request.url_for("get_user_role", uuid=uuid)


helpers.api_route_update(router, update_user_role)


#
# DELETE
#


def delete_user_role(uuid: UUID, db: Session = Depends(get_db)):
    try:
        if not crud.helpers.delete(uuid=uuid, db_table=UserRole, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to delete user role {uuid}")
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


helpers.api_route_delete(router, delete_user_role)
