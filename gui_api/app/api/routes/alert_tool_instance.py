from fastapi import APIRouter, Query
from typing import Optional

from api import db_api
from api.routes import helpers
from api_models.submission_tool_instance import SubmissionToolInstanceRead


router = APIRouter(
    prefix="/alert/tool/instance",
    tags=["Alert Tool Instance"],
)


#
# READ
#


def get_all_tool_instances(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/submission/tool/instance/?limit={limit}&offset={offset}")


helpers.api_route_read_all(router, get_all_tool_instances, SubmissionToolInstanceRead)
