from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.submission_tool import SubmissionToolRead


router = APIRouter(
    prefix="/alert/tool",
    tags=["Alert Tool"],
)


#
# READ
#


def get_all_tools(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/submission/tool/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_tools, SubmissionToolRead)
