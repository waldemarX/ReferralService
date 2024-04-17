from fastapi import APIRouter

from app.api_v1 import links_rst


general_router_v1 = APIRouter(tags=["API v1"], prefix="/api")


general_router_v1.include_router(
    links_rst.router,
    prefix="/link-generation",
)
