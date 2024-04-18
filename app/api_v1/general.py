from fastapi import APIRouter

from app.api_v1 import referrals_rst, token_rst


general_router_v1 = APIRouter(tags=["API v1"], prefix="/api")


general_router_v1.include_router(
    token_rst.router,
    prefix="/token",
)

general_router_v1.include_router(
    referrals_rst.router,
    prefix="/referrals/{code}",
)
