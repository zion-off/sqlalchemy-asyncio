from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import SessionAsync

security = HTTPBasic()

async def get_db():
    session = SessionAsync()
    try:
        yield session
    except:
        await session.rollback()
        raise
    else:
        await session.commit()
    finally:
        await session.close()


async def get_requesting_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        session: AsyncSession = Depends(get_db)):
    # TODO
    # find if any user exists in the database with email == credentials.username
    # check if user.password_hash == userservice.hash_password(credentials.password)
    # if true, return the user
    # else raise exception
    pass
