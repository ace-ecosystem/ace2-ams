from sqlalchemy.orm import Session
from typing import Optional

from api_models.queue import QueueCreate
from api_models.user import UserCreate
from api_models.user_role import UserRoleCreate
from db import crud


def create(
    username: str,
    db: Session,
    alert_queue: str = "external",
    display_name: str = "Analyst",
    email: Optional[str] = None,
    enabled: bool = True,
    event_queue: str = "external",
    history_username: Optional[str] = None,
    password: str = "asdfasdf",
    refresh_token: str = "asdf",
    roles: list[str] = None,
):
    crud.queue.create_or_read(model=QueueCreate(value=alert_queue), db=db)
    crud.queue.create_or_read(model=QueueCreate(value=event_queue), db=db)

    if email is None:
        email = f"{username}@test.com"

    if roles is None:
        roles = ["test_role"]

    for role in roles:
        crud.user_role.create_or_read(UserRoleCreate(value=role), db=db)

    user = crud.user.create_or_read(
        model=UserCreate(
            default_alert_queue=alert_queue,
            default_event_queue=event_queue,
            display_name=display_name,
            email=email,
            enabled=enabled,
            password=password,
            roles=roles,
            username=username,
        ),
        db=db,
    )

    # if history_username:
    #     crud.record_create_history(
    #         history_table=UserHistory,
    #         action_by=obj,
    #         record=obj,
    #         db=db,
    #     )

    return user
