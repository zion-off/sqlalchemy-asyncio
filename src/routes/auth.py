from fastapi import APIRouter, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.auth import LoginPayload, LoginResponse
from src.schemas.user import UserResponse
from src.dependencies import get_db
from src.auth.cookie import cookie_check


from ..services.auth import AuthService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

auth_service = AuthService()


@router.post("", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def authenticate_user(
    body: LoginPayload, response: Response, session: AsyncSession = Depends(get_db)
):
    return await auth_service.authenticate_user(
        response=response, session=session, body=body
    )


@router.get("", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def check_logged_in_user(
    session: AsyncSession = Depends(get_db), token: str | None = Depends(cookie_check)
):
    return await auth_service.get_logged_in_user(session, token)


@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response, token: str | None = Depends(cookie_check)):
    return await auth_service.logout_user(response=response, token=token)
