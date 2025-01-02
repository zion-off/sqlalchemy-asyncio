from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from .base import Base

class Message(Base):
    __tablename__ = "messages"


    user_id: str
    message: str
    created_at: datetime

    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
