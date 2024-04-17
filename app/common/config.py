from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import MetaData, NullPool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)

from app.common.sqla import MappingBase


current_directory: Path = Path.cwd()
load_dotenv(current_directory / ".env")

DATABASE_MIGRATED: bool = getenv("DATABASE_MIGRATED", "0") == "1"
PRODUCTION_MODE: bool = getenv("PRODUCTION", "0") == "1"
DB_URL: str = getenv(
    "DB_LINK", "postgresql+asyncpg://test:test@localhost:5432/test"
)
DB_SCHEMA: str | None = getenv("DB_SCHEMA", None)


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


engine = create_async_engine(
    DB_URL,
    pool_recycle=280,
    echo=not PRODUCTION_MODE,
    poolclass=None if PRODUCTION_MODE else NullPool,
)
db_meta = MetaData(naming_convention=convention, schema=DB_SCHEMA)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase, MappingBase):
    __tablename__: str
    __abstract__: bool

    metadata = db_meta
