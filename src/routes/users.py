
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.common import CommonFilters
from src.schemas.user import UserCreatePayload, UserResponse
from src.dependencies import get_db


from ..services.users import UserService

router = APIRouter(prefix="/api/users")

user_service = UserService()


@router.get("")
async def list_users(filters: CommonFilters, session: AsyncSession = Depends(get_db)):
    return await user_service.list_users(session=session, filters=filters)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_users(body: UserCreatePayload, session: AsyncSession = Depends(get_db)):
    return await user_service.create_user(session=session, body=body)


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    pass
