from fastapi import APIRouter, status, Depends, Header
from typing import List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db
from src.schemas.common import CommonFilters
from src.auth.cookie import cookie_check
from src.schemas.room import RoomSchema, RoomCreatePayload
from src.routes.messages import router as messages_router

from ..services.rooms import RoomService

router = APIRouter(
    prefix="/api/rooms", tags=["Rooms"]
)

router.include_router(messages_router)

room_service = RoomService()


@router.get("", response_model=List[RoomSchema], status_code=status.HTTP_200_OK)
async def list_rooms(filters: CommonFilters, session: AsyncSession = Depends(get_db), token: str | None = Depends(cookie_check), user_agent: Annotated[str | None, Header()] = None):
    return await room_service.list_rooms(session=session, filters=filters, token=token, user_agent=user_agent)


@router.post("", response_model=RoomSchema, status_code=status.HTTP_201_CREATED)
async def create_rooms(
    request: RoomCreatePayload,
    session: AsyncSession = Depends(get_db),
    token: str | None = Depends(cookie_check),
):
    return await room_service.create_room(
        session=session, token=token, room_name=request.room_name
    )



