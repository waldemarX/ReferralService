from fastapi import APIRouter
from app.dependencies.token_dep import TargetToken, TokenResponses
from app.utils.referrals import (
    get_full_referral_tree,
    get_list_of_referrals,
    get_referral_parents_tree,
)
from app.models.token_db import Token

router = APIRouter()


@router.get(
    path="/full",
    responses=TokenResponses.responses(),
    summary="Retrieve full referral tree",
)
async def get_referral_tree(token: TargetToken):
    return await get_full_referral_tree(token)


@router.get(
    path="/list",
    responses=TokenResponses.responses(),
    summary="Retrieve referral list",
)
async def get_referral_list(token: TargetToken):
    return await get_list_of_referrals(token)


@router.get(
    path="/parents",
    responses=TokenResponses.responses(),
    summary="Retrieve referral parents",
)
async def get_referral_parents(token: TargetToken):
    return await get_referral_parents_tree(token)


@router.get(
    path="/test",
    responses=TokenResponses.responses(),
    summary="test req",
)
async def get_req(token: TargetToken):
    req = await Token.get_referral_parents(token.code)
    return {"result": f"{req.fetchall()}"}
