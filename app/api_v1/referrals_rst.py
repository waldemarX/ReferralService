from fastapi import APIRouter
from app.dependencies.token_dep import TargetToken, TokenResponses
from app.utils.referrals import (
    get_full_referral_tree,
    get_referrals,
    get_referral_parents,
)

router = APIRouter()


@router.get(
    path="/tree",
    responses=TokenResponses.responses(),
    summary="Retrieve full referral tree",
)
async def retrieve_referral_tree(token: TargetToken):
    return await get_full_referral_tree(token)


@router.get(
    path="/list",
    responses=TokenResponses.responses(),
    summary="Retrieve referral list",
)
async def retrieve_referral_list(token: TargetToken):
    return await get_referrals(token)


@router.get(
    path="/parents",
    responses=TokenResponses.responses(),
    summary="Retrieve referral parents",
)
async def retrieve_referral_parents(token: TargetToken):
    return await get_referral_parents(token)
