from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from sqlalchemy.orm import relationship
from typing import List
from .base import Base
from .room import Room

class User(Base):
    __tablename__ = "users"
    
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    rooms: Mapped[List[Room]] = relationship("Room", back_populates="user")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="user")
