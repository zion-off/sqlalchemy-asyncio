from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base

class Message(Base):
    __tablename__ = "messages"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    message: Mapped[str] = mapped_column(String(120), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="messages")
    room: Mapped["Room"] = relationship("Room", back_populates="messages")
