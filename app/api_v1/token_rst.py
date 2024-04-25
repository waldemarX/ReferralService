from fastapi import APIRouter

from app.dependencies.token_dep import TargetToken, TokenResponses
from app.models.token_db import Token

router = APIRouter()


@router.post(
    path="/",
    response_model=Token.FullModel,
    summary="Generate referral token",
)
async def create_token(data: Token.CreateModel):
    token = await Token.create(**data.model_dump())
    return token


@router.get(
    path="/{code}/",
    response_model=Token.FullModel,
    responses=TokenResponses.responses(),
    summary="Retrieve referral token information",
)
async def retrieve_token_information(token: TargetToken):
    return token


@router.delete(
    path="/{code}/",
    status_code=204,
    responses=TokenResponses.responses(),
    summary="Delete token",
)
async def delete_token(token: TargetToken):
    await token.delete()
