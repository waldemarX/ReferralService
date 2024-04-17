from fastapi import APIRouter

from app.models.links_db import Link, LinkMode


router = APIRouter()


@router.get(
    path="/",
    summary="Generate new referral token",
)
async def create_referral_link(mode: LinkMode):
    link = await Link.create()
    return {"link_token": link.token, "link_mode": mode}
