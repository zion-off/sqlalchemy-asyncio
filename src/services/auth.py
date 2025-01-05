from sqlalchemy import select
from fastapi import HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.schemas.auth import LoginPayload, LoginResponse
from src.auth.cookie import cookie_decrypt


class AuthService:
    def cookie_generator(self, value) -> str:
        return f"#{value}#"

    async def authenticate_user(
        self, response: Response, body: LoginPayload, session: AsyncSession
    ):
        stm = select(User).filter(User.email == body.email)
        res = await session.execute(stm)
        user = res.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        elif user.password_hash[1:-1] == body.password:
            response.set_cookie(
                key="token",
                value=self.cookie_generator(user.id),
                httponly=True,
                max_age=3600,
            )
            return LoginResponse(message="Authenticated")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

    async def get_logged_in_user(self, session: AsyncSession, token: str | None):
        if token:
            print(token)
            id = await cookie_decrypt(token)
            user = await session.get(User, id)
            if user:
                return await session.get(User, id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not currently logged in",
            )

    async def logout_user(self, response: Response, token: str | None):
        if token:
            response.delete_cookie("token")
            print(token)
            return LoginResponse(message="Logged out")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not currently logged in",
            )
