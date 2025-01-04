from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.models.base import engine, Base
from src.routes.users import router as user_router
from src.routes.rooms import router as room_router
from src.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Message Server", lifespan=lifespan)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(room_router)


async def init_db():
    # "begin once" https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
