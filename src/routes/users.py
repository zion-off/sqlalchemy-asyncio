from fastapi import APIRouter, status, Depends, Header
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.common import CommonFilters
from src.schemas.user import UserCreatePayload, UserResponse, UserUpdatePayload
from src.dependencies import get_db
from src.auth.bearer import JWTBearer


from ..services.users import UserService

router = APIRouter(prefix="/api/users", tags=["Users"])

user_service = UserService()


@router.get("")
async def list_users(filters: CommonFilters, session: AsyncSession = Depends(get_db)):
    return await user_service.list_users(session=session, filters=filters)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_users(
    body: UserCreatePayload, session: AsyncSession = Depends(get_db)
):
    return await user_service.create_user(session=session, body=body)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: str,
    session: AsyncSession = Depends(get_db),
    token: str | None = Depends(JWTBearer()),
    user_agent: Annotated[str | None, Header()] = None,
):
    return await user_service.get_user_by_id(
        session=session, user_id=user_id, token=token, user_agent=user_agent
    )


@router.patch(
    "/{user_id}", response_model=UserCreatePayload, status_code=status.HTTP_200_OK
)
async def update_user_by_id(
    body: UserUpdatePayload,
    user_id: str,
    session: AsyncSession = Depends(get_db),
    token: str | None = Depends(JWTBearer()),
    user_agent: Annotated[str | None, Header()] = None,
):
    return await user_service.update_user(
        body=body, user_id=user_id, session=session, token=token, user_agent=user_agent
    )
