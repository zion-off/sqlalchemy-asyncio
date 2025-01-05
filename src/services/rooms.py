from fastapi import HTTPException, status
from sqlalchemy import select, desc
from src.schemas.common import CommonFilters
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.room import Room
from src.auth.cookie import cookie_decrypt, is_polite


class RoomService:
    async def create_room(
        self, session: AsyncSession, token: str | None, room_name: str
    ):
        if token:
            room = Room(room_name=room_name, created_by=cookie_decrypt(token))
            session.add(room)
            await session.flush()
            return room
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    async def list_rooms(
        self,
        session: AsyncSession,
        filters: CommonFilters,
        token: str | None,
        user_agent: str | None,
    ):
        if token or is_polite(user_agent):
            stm = select(Room).offset(filters.offset).limit(filters.page_size)
            if filters.sort_by:
                stm = (
                    stm.order_by(desc(filters.sort_by))
                    if filters.order == "desc"
                    else stm.order_by(filters.sort_by)
                )
            res = await session.execute(statement=stm)
            return res.scalars().all()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
