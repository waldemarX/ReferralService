from fastapi import APIRouter
from starlette.status import HTTP_409_CONFLICT

from app.common.responses import Responses
from app.dependencies.magic import include_responses
from app.dependencies.token_dep import (
    TargetToken,
    TokenResponses,
    is_name_unique,
)
from app.models.token_db import Token, TokenMode


router = APIRouter()


@include_responses(TokenResponses)
class TokenNameResponses(Responses):
    NAME_IN_USE = (HTTP_409_CONFLICT, "Referral token name already in use")


@router.post(
    path="/",
    response_model=Token.FullModel,
    summary="Generate referral token",
)
async def create_token():
    token = await Token.create()
    return token


@router.get(
    path="/{code}/",
    response_model=Token.FullModel,
    responses=TokenResponses.responses(),
    summary="Retrieve referral token information",
)
async def get_token_information(code: str):
    token = await Token.find_first_by_kwargs(code=code)
    if token is None:
        raise TokenResponses.TOKEN_NOT_FOUND.value
    return token


@router.patch(
    path="/{code}/name/",
    response_model=Token.FullModel,
    responses=TokenNameResponses.responses(),
    summary="Change token name",
)
async def update_token_name(code: str, name_data: Token.NameModel):
    token = await Token.find_first_by_kwargs(code=code)
    if token is None:
        raise TokenResponses.TOKEN_NOT_FOUND.value
    if not await is_name_unique(name_data.name, token.name):
        raise TokenNameResponses.NAME_IN_USE.value
    token.update(**name_data.model_dump(exclude_defaults=True))
    return token


@router.patch(
    path="/{code}/mode/",
    response_model=Token.FullModel,
    responses=TokenResponses.responses(),
    summary="Change token mode",
)
async def update_token_mode(code: str, mode: TokenMode):
    token = await Token.find_first_by_kwargs(code=code)
    if token is None:
        raise TokenResponses.TOKEN_NOT_FOUND.value
    token.update(mode=mode)
    return token


@router.delete(
    path="/{code}/",
    status_code=204,
    responses=TokenResponses.responses(),
    summary="Delete token",
)
async def delete_token(token: TargetToken):
    await token.delete()
