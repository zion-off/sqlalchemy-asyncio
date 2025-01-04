from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserCreatePayload(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdatePayload(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
