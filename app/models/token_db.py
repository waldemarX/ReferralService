import enum
from secrets import token_urlsafe
from typing import Annotated, Any, ClassVar, Self
from pydantic import StringConstraints, Field
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from pydantic_marshals.sqlalchemy import MappedModel

from app.common.config import Base


class TokenMode(str, enum.Enum):
    STANDART = "standart"
    RECURSIVE = "recursive"


class Token(Base):
    __tablename__ = "tokens"
    nbytes: ClassVar[int] = 8

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(11))
    name: Mapped[str | None] = mapped_column(
        String(30), default=None, unique=True
    )
    mode: Mapped[TokenMode] = mapped_column(
        Enum(TokenMode),
        default=TokenMode.STANDART,
    )

    NameType = Annotated[
        str | None,
        StringConstraints(strip_whitespace=True),
        Field(min_length=3, max_length=30),
    ]

    FullModel = MappedModel.create(columns=[code, (name, NameType), mode])
    NameModel = MappedModel.create(columns=[(name, NameType)])
    PatchModel = MappedModel.create(columns=[(name, NameType), mode])

    def generate_token() -> str:
        return token_urlsafe(Token.nbytes)

    @classmethod
    async def create(cls, **kwargs: Any) -> Self:
        if kwargs.get("code") is None:
            code = cls.generate_token()
            if (await Token.find_first_by_kwargs(code=code)) is not None:
                raise RuntimeError("Token collision happened")
            kwargs["code"] = code
        return await super().create(**kwargs)
