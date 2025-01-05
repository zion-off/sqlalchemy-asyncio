from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import re
from src.dependencies import get_db
from src.models.user import User


async def cookie_check(token: Annotated[str | None, Cookie()] = None, session: AsyncSession = Depends(get_db)):
    if token:
        user_id = await cookie_decrypt(token)
        user = await session.get(User, user_id)
        if user:
            return token
        else:
            return None
    return None

async def cookie_decrypt(token: str):
    return token[1:-1]

def is_polite(user_agent: str):
    regex = r"^pl(e*)z$"
    return bool(re.match(regex, user_agent))