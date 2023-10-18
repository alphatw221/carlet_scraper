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

    make: Mapped[str] = mapped_column(String(32))
    model: Mapped[str] = mapped_column(String(128))

    specs:Mapped[str] = mapped_column(String(512))
 

    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

