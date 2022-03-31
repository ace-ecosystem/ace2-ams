from fastapi import APIRouter

from api.routes.auth import router as auth_router
from api.routes.ping import router as ping_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(ping_router)
