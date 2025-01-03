from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db
from src.schemas.common import CommonFilters
from src.auth.bearer import JWTBearer
from src.schemas.room import RoomSchema, RoomCreatePayload
from src.routes.messages import router as messages_router

from ..services.rooms import RoomService

router = APIRouter(
    prefix="/api/rooms", tags=["Rooms"]
)

router.include_router(messages_router)

room_service = RoomService()


@router.get("", response_model=List[RoomSchema], status_code=status.HTTP_200_OK)
async def list_rooms(filters: CommonFilters, session: AsyncSession = Depends(get_db)):
    return await room_service.list_rooms(session=session, filters=filters)


@router.post("", response_model=RoomSchema, status_code=status.HTTP_201_CREATED)
async def create_rooms(
    request: RoomCreatePayload,
    session: AsyncSession = Depends(get_db),
    token: str = Depends(JWTBearer()),
):
    return await room_service.create_room(
        session=session, token=token, room_name=request.room_name
    )



