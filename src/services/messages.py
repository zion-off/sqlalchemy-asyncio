from sqlalchemy import select, desc, delete, update
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.message import Message
from src.schemas.message import (
    MessageCreateRequest,
    MessageCreateResponse,
    MessageUpdateRequest,
    MessageUpdateResponse,
)
from src.schemas.common import CommonFilters
from src.auth.handler import decode_jwt, is_polite


class MessageService:
    async def create_message(
        self,
        body: MessageCreateRequest,
        session: AsyncSession,
        room_id: str,
        token: str | None,
    ):
        if token:
            token = decode_jwt(token)
            message = Message(
                user_id=token.get("user_id"), room_id=room_id, message=body.message
            )
            session.add(message)
            await session.flush()
            return MessageCreateResponse(
                user_id=message.user_id,
                room_id=message.room_id,
                message_id=message.id,
                message=message.message,
                created_at=message.created_at,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    async def list_messages(
        self,
        filters: CommonFilters,
        session: AsyncSession,
        room_id: str,
        token: str | None,
        user_agent: str | None,
    ):
        if token or is_polite(user_agent):
            stm = (
                select(Message)
                .where(Message.room_id == room_id)
                .offset(filters.offset)
                .limit(filters.page_size)
            )
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

    async def delete_messages(
        self,
        session: AsyncSession,
        user_agent: str | None,
        room_id: str,
        message_id: str,
        token: str | None,
    ):
        stm = select(Message).where(
            (Message.room_id == room_id) & (Message.id == message_id)
        )
        res = await session.execute(statement=stm)
        message = res.scalars().first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )
        if not is_polite(user_agent) and (
            message.user_id != decode_jwt(token).get("user_id")
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
            )
        delete_stm = delete(Message).where(
            Message.room_id == room_id, Message.id == message_id
        )
        await session.execute(statement=delete_stm)
        return {"message": "Deleted message"}

    async def update_message(
        self,
        body: MessageUpdateRequest,
        session: AsyncSession,
        user_agent: str | None,
        room_id: str,
        message_id: str,
        token: str,
    ):
        stm = select(Message).where(
            Message.room_id == room_id, Message.id == message_id
        )
        res = await session.execute(statement=stm)
        message = res.scalar_one_or_none()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found",
            )
        if not is_polite(user_agent) and (
            message.user_id != decode_jwt(token).get("user_id")
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
            )
        old_message = message.message
        message.message = body.new_message
        return MessageUpdateResponse(
            message_id=message.id,
            room_id=message.room_id,
            old_message=old_message,
            updated_message=body.new_message,
        )
