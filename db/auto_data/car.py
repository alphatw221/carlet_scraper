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
    model_category = mapped_column(String(128))
    model: Mapped[str] = mapped_column(String(128))
    sub_model: Mapped[str] = mapped_column(String(128))
    
    link: Mapped[str] = mapped_column(String(255), nullable=True)

    start_of_perduction_year:Mapped[int] = mapped_column(Integer(), nullable=True)
    end_of_perduction_year:Mapped[int] = mapped_column(Integer(), nullable=True)

    properties = relationship('Property', back_populates='car')

    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Property(Base):

    __tablename__ = "property"

    id: Mapped[int] = mapped_column(primary_key=True)

    name = mapped_column(String(255), nullable=True)
    value:Mapped[str] = mapped_column(String(512), nullable=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=True)
    car: Mapped["Car"] = relationship(back_populates="properties")

    created_at = mapped_column(DateTime, default=datetime.utcnow)
    updated_at = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

