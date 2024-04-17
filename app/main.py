from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from collections.abc import Awaitable, Callable, AsyncIterator
from starlette.requests import Request
from starlette.responses import Response
from contextlib import asynccontextmanager

from app.api_v1.general import general_router_v1
from app.common.config import DATABASE_MIGRATED, PRODUCTION_MODE, sessionmaker
from app.common.sqla import session_context
from app.utils.setup import reinit_database


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if not PRODUCTION_MODE and not DATABASE_MIGRATED:
        await reinit_database()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general_router_v1)


@app.middleware("http")
async def database_session_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    async with sessionmaker.begin() as session:
        session_context.set(session)
        return await call_next(request)
