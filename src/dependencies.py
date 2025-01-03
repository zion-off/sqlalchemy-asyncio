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


