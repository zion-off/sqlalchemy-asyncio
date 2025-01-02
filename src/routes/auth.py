from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.auth import LoginPayload, LoginResponse
from src.dependencies import get_db


from ..services.auth import AuthService

router = APIRouter(prefix="/api/auth")

auth_service = AuthService()

@router.post("", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def authenticate_user(body: LoginPayload, session: AsyncSession = Depends(get_db)):
    return await auth_service.authenticate_user(session=session, body=body)