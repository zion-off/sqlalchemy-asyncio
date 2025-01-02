from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserCreatePayload
from src.schemas.common import CommonFilters

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
            stm = stm.order_by(desc(filters.sort_by)) if filters.order == "desc" else stm.order_by(filters.sort_by)
        res = await session.execute(statement=stm)
        return res.scalars().all()

    async def get_user_by_id(self, user_id: int):
        pass

