from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.schemas.auth import LoginPayload, LoginResponse
from ..auth.handler import sign_jwt


class AuthService:
    async def authenticate_user(self, body: LoginPayload, session: AsyncSession):
        stm = select(User).filter(User.email == body.email)
        res = await session.execute(stm)
        user = res.scalar_one()
        if user.password_hash[1:-1] == body.password:
            gen_token = sign_jwt(user.id)
            return LoginResponse(access_token=gen_token.get("access_token"))
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
