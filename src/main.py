from fastapi import FastAPI
from src.models.base import engine, Base
from src.routes.users import router as user_router
from src.routes.rooms import router as room_router


app = FastAPI(
    title="Message Server",
)
app.include_router(user_router)
app.include_router(room_router)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)