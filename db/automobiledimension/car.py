from . import Base, engine

from typing import List
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Integer, String, ForeignKey, Uuid, Date, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import UniqueConstraint





class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    
    make_name: Mapped[str] = mapped_column(String(32), default=None, nullable=True)
    make: Mapped[str] = mapped_column(String(32))

    year: Mapped[int] = mapped_column(Integer())
    
    model_name: Mapped[str] = mapped_column(String(128), default=None, nullable=True)
    model: Mapped[str] = mapped_column(String(128))

    image_src: Mapped[str] = mapped_column(String(255))

    length: Mapped[str] = mapped_column(String(128), default=None, nullable=True)
    height: Mapped[str] = mapped_column(String(128), default=None, nullable=True)
    width: Mapped[str] = mapped_column(String(128), default=None, nullable=True)

    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

