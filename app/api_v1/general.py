from fastapi import APIRouter

from app.api_v1 import token_generation


general_router = APIRouter(tags=["API v1"], prefix="/api")


general_router.include_router(
    token_generation.router,
    prefix="/link-generation",
)
