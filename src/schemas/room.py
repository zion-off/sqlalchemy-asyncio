from datetime import datetime
from pydantic import BaseModel

class RoomSchema(BaseModel):
    room_name: str
    created_by: str

class RoomCreatePayload(BaseModel):
    room_name: str


class RoomResponse(BaseModel):
    room_id: str
    created_at: datetime
