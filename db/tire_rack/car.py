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
    sub_model: Mapped[str] = mapped_column(String(255))

    tire_sizes = relationship('TireSize', back_populates='car')
    wipers = relationship('Wiper', back_populates='car')

    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scraped_at = mapped_column(DateTime, nullable=True, default=None)

class TireSize(Base):

    __tablename__ = "tire_size"

    id: Mapped[int] = mapped_column(primary_key=True)

    additional_info = mapped_column(String(255), nullable=True)
    size:Mapped[str] = mapped_column(String(255), nullable=True)
    front_size:Mapped[str] = mapped_column(String(255), nullable=True)
    rear_size:Mapped[str] = mapped_column(String(255), nullable=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=True)
    car: Mapped["Car"] = relationship(back_populates="tire_sizes")

    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Wiper(Base):

    __tablename__ = "wiper"

    id: Mapped[int] = mapped_column(primary_key=True)

    additional_info = mapped_column(String(255), nullable=True)
    manufacturer_part:Mapped[str] = mapped_column(String(255), nullable=True)
    note:Mapped[str] = mapped_column(String(255), nullable=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=True)
    car: Mapped["Car"] = relationship(back_populates="wipers")

    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
