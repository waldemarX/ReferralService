import enum
from secrets import token_urlsafe
from typing import Any, ClassVar, Self
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.config import Base


class LinkMode(str, enum.Enum):
    STANDART = "standart"
    RECURSIVE = "recursive"


class Link(Base):
    __tablename__ = "links"
    token_bytes: ClassVar[int] = 64

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(100))
    mode: Mapped[LinkMode] = mapped_column(
        Enum(LinkMode),
        default=LinkMode.STANDART,
    )

    def generate_token() -> str:
        return token_urlsafe(Link.token_bytes)

    @classmethod
    async def create(cls, **kwargs: Any) -> Self:
        if kwargs.get("token") is None:
            token = cls.generate_token()
            if (await Link.find_first_by_kwargs(token=token)) is not None:
                raise RuntimeError("Token collision happened")
            kwargs["token"] = token
        return await super().create(**kwargs)
