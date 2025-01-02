from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from ..auth.handler import sign_jwt


class AuthService:
    async def authenticate_user(self, session: AsyncSession, email: str, password: str):
        stm = select(User).filter(User.email == email)
        res = await session.execute(stm).scalar_one()
        if res.password_hash == password:
            return sign_jwt(res.id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
