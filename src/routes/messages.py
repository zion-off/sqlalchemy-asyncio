from fastapi import APIRouter, status, Path, Depends, Header
from typing import List, Annotated
from src.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.cookie import cookie_check
from src.schemas.common import CommonFilters
from src.schemas.message import (
    MessageSchema,
    MessageCreateRequest,
    MessageCreateResponse,
    MessageUpdateRequest,
    MessageUpdateResponse,
)
from ..services.messages import MessageService

router = APIRouter(prefix="/{room_id}/messages", tags=["Messages"])

message_service = MessageService()


@router.post("", response_model=MessageCreateResponse)
async def send_message(
    body: MessageCreateRequest,
    session: AsyncSession = Depends(get_db),
    room_id: str = Path(...),
    token: str | None = Depends(cookie_check),
):
    return await message_service.create_message(
        body=body, session=session, room_id=room_id, token=token
    )


@router.get("", response_model=List[MessageSchema])
async def get_messages(
    filters: CommonFilters,
    session: AsyncSession = Depends(get_db),
    room_id: str = Path(...),
    token: str | None = Depends(cookie_check),
    user_agent: Annotated[str | None, Header()] = None,
):
    return await message_service.list_messages(
        filters=filters,
        session=session,
        room_id=room_id,
        token=token,
        user_agent=user_agent,
    )


@router.delete("/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(
    session: AsyncSession = Depends(get_db),
    room_id: str = Path(...),
    message_id: str = Path(...),
    token: str | None = Depends(cookie_check),
    user_agent: Annotated[str | None, Header()] = None,
):
    return await message_service.delete_messages(
        session=session,
        user_agent=user_agent,
        room_id=room_id,
        message_id=message_id,
        token=token,
    )


@router.patch(
    "/{message_id}",
    response_model=MessageUpdateResponse,
)
async def update_message(
    body: MessageUpdateRequest,
    session: AsyncSession = Depends(get_db),
    room_id: str = Path(...),
    message_id: str = Path(...),
    token: str | None = Depends(cookie_check),
    user_agent: Annotated[str | None, Header()] = None,
):
    return await message_service.update_message(
        body=body,
        session=session,
        user_agent=user_agent,
        room_id=room_id,
        message_id=message_id,
        token=token,
    )
