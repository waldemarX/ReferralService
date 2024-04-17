from typing import Annotated
from fastapi import Depends, Path
from starlette.status import HTTP_404_NOT_FOUND
from pydantic_marshals.base import PatchDefault, PatchDefaultType

from app.common.responses import Responses
from app.models.token_db import Token


class TokenResponses(Responses):
    TOKEN_NOT_FOUND = (HTTP_404_NOT_FOUND, "Referral token not found")


async def is_name_unique(
    patch_name: str | PatchDefaultType, current_name: str
) -> bool:
    if patch_name is not PatchDefault and patch_name != current_name:
        return await Token.find_first_by_kwargs(name=patch_name) is None
    return True


async def get_token(code: Annotated[str, Path()]) -> Token:
    token = await Token.find_first_by_kwargs(code=code)
    if token is None:
        raise TokenResponses.TOKEN_NOT_FOUND.value
    return token


TargetToken = Annotated[Token, Depends(get_token)]
