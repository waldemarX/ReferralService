from fastapi import APIRouter
from secrets import token_urlsafe


router = APIRouter()


@router.get(
    path="/",
    summary="Generate new test referral token",
)
async def generate_token():
    link_token = token_urlsafe(64)
    return {"link_token": link_token}
