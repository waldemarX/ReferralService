from datetime import datetime
from secrets import token_urlsafe
from typing import Annotated, Any, ClassVar, Self
from pydantic import Field, StringConstraints
from sqlalchemy import String, TIMESTAMP, select
from sqlalchemy.orm import Mapped, mapped_column
from pydantic_marshals.sqlalchemy import MappedModel

from app.common.config import Base
from app.common.sqla import db


class Token(Base):
    __tablename__ = "tokens"
    nbytes: ClassVar[int] = 32

    code: Mapped[str] = mapped_column(String(44), primary_key=True)
    identity: Mapped[str] = mapped_column(String(150))
    invitee_code: Mapped[str | None] = mapped_column(String(44), default=None)
    joined: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, nullable=False
    )

    IdentityType = Annotated[
        str,
        StringConstraints(strip_whitespace=True),
        Field(min_length=3, max_length=150),
    ]

    FullModel = MappedModel.create(
        columns=[code, identity, joined, invitee_code]
    )
    CreateModel = MappedModel.create(
        columns=[(identity, IdentityType), invitee_code]
    )

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

    @classmethod
    async def get_referral_list(cls, code: str) -> Self | None:
        return await db.get_all(select(cls).filter_by(invitee_code=code))

    @classmethod
    async def get_referral_parent_list(cls, code: str) -> list[tuple]:
        anchor = (
            select(
                cls.code,
                cls.identity,
                cls.invitee_code,
                cls.joined,
            )
            .where(cls.code == code)
            .cte(recursive=True)
        )
        recursive_part = anchor.union_all(
            select(
                cls.code,
                cls.identity,
                cls.invitee_code,
                cls.joined,
            ).where(anchor.c.invitee_code == cls.code)
        )
        statement = select(
            recursive_part.c.code,
            recursive_part.c.identity,
            recursive_part.c.invitee_code,
            recursive_part.c.joined,
        ).filter(recursive_part.c.code != code)

        return await db.session.execute(statement)

    @classmethod
    async def get_referral_tree_list(cls, code: str) -> list[tuple]:
        anchor = (
            select(
                cls.code,
                cls.identity,
                cls.invitee_code,
                cls.joined,
            )
            .where(cls.code == code)
            .cte(recursive=True)
        )
        recursive_part = anchor.union_all(
            select(
                cls.code,
                cls.identity,
                cls.invitee_code,
                cls.joined,
            ).join(anchor, anchor.c.code == cls.invitee_code)
        )
        statement = select(
            recursive_part.c.code,
            recursive_part.c.identity,
            recursive_part.c.invitee_code,
            recursive_part.c.joined,
        )

        result = await db.session.execute(statement)
        return result.fetchall()
