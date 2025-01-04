from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, String
from typing import List
from sqlalchemy.orm import relationship
from .base import Base

class Room(Base):
    __tablename__ = "rooms"
    room_name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="rooms")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="room")
