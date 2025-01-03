from datetime import datetime
from pydantic import BaseModel


class MessageSchema(BaseModel):
    user_id: str
    room_id: str
    message: str


class MessageCreateRequest(BaseModel):
    message: str

    class Config:
        from_attributes = True


class MessageCreateResponse(BaseModel):
    user_id: str
    room_id: str
    message_id: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageUpdateRequest(BaseModel):
    new_message: str

    class Config:
        from_attributes = True


class MessageUpdateResponse(BaseModel):
    message_id: str
    room_id: str
    old_message: str
    updated_message: str

    class Config:
        from_attributes = True
