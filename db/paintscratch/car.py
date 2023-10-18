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
    year: Mapped[int] = mapped_column(Integer())
    model: Mapped[str] = mapped_column(String(128))

    paints = relationship('Paint', back_populates='car')


    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Paint(Base):

    __tablename__ = "paint"

    id: Mapped[int] = mapped_column(primary_key=True)

    color = mapped_column(String(255), nullable=True)
    code:Mapped[str] = mapped_column(String(255), nullable=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=True)
    car: Mapped["Car"] = relationship(back_populates="paints")

    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

