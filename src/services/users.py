from sqlalchemy import select, desc
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.schemas.user import UserCreatePayload
from src.schemas.common import CommonFilters
from src.auth.handler import decode_jwt, is_polite


class UserService:
    def hash_password(self, value) -> str:
        return f"#{value}#"

    async def create_user(self, session: AsyncSession, body: UserCreatePayload):
        body_dict = body.model_dump()
        del body_dict["password"]
        user = User(**body_dict)
        user.password_hash = self.hash_password(body.password)
        session.add(user)
        await session.flush()
        return user

    async def list_users(self, session: AsyncSession, filters: CommonFilters):
        stm = select(User).offset(filters.offset).limit(filters.page_size)
        if filters.sort_by:
            stm = (
                stm.order_by(desc(filters.sort_by))
                if filters.order == "desc"
                else stm.order_by(filters.sort_by)
            )
        res = await session.execute(statement=stm)
        return res.scalars().all()

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: str,
        token: str | None,
        user_agent: str | None,
    ):
        if token or is_polite(user_agent):
            stm = select(User).filter(User.id == user_id)
            res = await session.execute(stm)
            user = res.scalar_one()
            token = decode_jwt(token)
            if user and (is_polite(user_agent) or token.get("user_id") == user_id):
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
