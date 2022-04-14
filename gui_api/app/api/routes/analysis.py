from fastapi import APIRouter
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.analysis import AnalysisRead


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


#
# READ
#


def get_analysis(uuid: UUID):
    return db_api.get(path=f"/analysis/{uuid}")


helpers.api_route_read(router, get_analysis, AnalysisRead)
