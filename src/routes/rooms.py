from fastapi import APIRouter, status, Depends
from src.dependencies import get_requesting_user

router = APIRouter(prefix="/api/rooms", dependencies=[Depends(get_requesting_user)])


@router.get("")
async def list_rooms():
    pass
