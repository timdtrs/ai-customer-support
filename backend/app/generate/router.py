from fastapi import APIRouter

from . import generate


router = APIRouter()

router.include_router(generate.router, prefix="/generate", tags=["generate"])
