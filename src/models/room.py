from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from .base import Base


class Room(Base):
    __tablename__ = "rooms"
    room_name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_by: Mapped[str] = mapped_column(String(120), nullable=False)
