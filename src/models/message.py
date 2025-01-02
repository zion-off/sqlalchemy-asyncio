from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from .base import Base


class Message(Base):
    __tablename__ = "messages"
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(String(120), nullable=False)
