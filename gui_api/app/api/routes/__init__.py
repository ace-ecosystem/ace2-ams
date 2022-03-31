from fastapi import APIRouter

from api.routes.ping import router as ping_router


router = APIRouter()

router.include_router(ping_router)
