import requests

from fastapi import APIRouter, HTTPException, status
from uuid import UUID

from api_models.analysis import AnalysisRead

from api.routes import helpers
from core.config import get_settings


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


#
# READ
#


def get_analysis(uuid: UUID):
    try:
        result = requests.get(
            f"{get_settings().database_api_url}/analysis/{uuid}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result.json()


helpers.api_route_read(router, get_analysis, AnalysisRead)
