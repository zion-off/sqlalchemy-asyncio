from pydantic import BaseModel

class RoomSchema(BaseModel):
    room_name: str
    created_by: str

class RoomCreatePayload(BaseModel):
    room_name: str

