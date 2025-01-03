from sqlalchemy import select, desc
from fastapi import HTTPException, status
from src.schemas.common import CommonFilters
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.room import Room
from src.auth.handler import decode_jwt


class RoomService:
    async def create_room(self, session: AsyncSession, token: str, room_name: str):
        token = decode_jwt(token)
        room = Room(room_name=room_name, created_by=token.user_id)
        session.add(room)
        await session.flush()
        return room

    async def list_rooms(self, session: AsyncSession, filters: CommonFilters):
        stm = select(Room).offset(filters.offset).limit(filters.page_size)
        if filters.sort_by:
            stm = (
                stm.order_by(desc(filters.sort_by))
                if filters.order == "desc"
                else stm.order_by(filters.sort_by)
            )
        res = await session.execute(statement=stm)
        return res.scalars().all()
