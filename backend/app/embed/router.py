from fastapi import APIRouter

from . import embed


router = APIRouter()

router.include_router(embed.router, prefix="/embed", tags=["embed"])
