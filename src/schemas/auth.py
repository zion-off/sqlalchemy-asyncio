from pydantic import BaseModel

class LoginPayload(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

