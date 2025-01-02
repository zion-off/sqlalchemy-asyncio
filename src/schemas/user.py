from datetime import datetime
from pydantic import BaseModel


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
