from datetime import datetime
from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str
    created_at: str


class MessageCreateRequest(BaseModel):
    user_id: int
    message: str

    class Config:
        from_attributes = True


class MessageCreateResponse(BaseModel):
    user_id: int
    message_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageUpdateRequest(BaseModel):
    message_id: int
    new_message: str

    class Config:
        from_attributes = True


class MessageUpdateResponse(BaseModel):
    message_id: int
    old_message: str
    update_message: str
    modified_at: datetime

    class Config:
        from_attributes = True

class MessageDeleteRequest(BaseModel):
    message_id: int

    
