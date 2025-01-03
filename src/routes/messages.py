from fastapi import APIRouter, status, Path, Depends
from typing import List
from src.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.bearer import JWTBearer
from src.schemas.message import (
    MessageSchema,
    MessageCreateRequest,
    MessageCreateResponse,
    MessageUpdateRequest,
    MessageUpdateResponse,
)

router = APIRouter(prefix="/{room_id}/messages", tags=["Messages"])


@router.post(
    "", dependencies=[Depends(JWTBearer())], response_model=MessageCreateResponse
)
async def send_message(body: MessageCreateRequest, room_id: int = Path(...)):
    pass


@router.get("", dependencies=[Depends(JWTBearer())], response_model=List[MessageSchema])
async def get_messages(
    room_id: int = Path(...), session: AsyncSession = Depends(get_db)
):
    pass


@router.delete(
    "/{message_id}",
    status_code=status.HTTP_200_OK
)
async def delete_message(
    room_id: int = Path(...),
    message_id: int = Path(...),
    session: AsyncSession = Depends(get_db),
    token: str = Depends(JWTBearer()),
):
    pass


@router.patch(
    "/{message_id}",
    response_model=MessageUpdateResponse,
)
async def update_message(
    body: MessageUpdateRequest,
    room_id: int = Path(...),
    message_id: int = Path(...),
    session: AsyncSession = Depends(get_db),
    token: str = Depends(JWTBearer()),
):
    pass
