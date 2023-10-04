from . import Base, engine

from typing import List
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Integer, String, ForeignKey, Uuid, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import UniqueConstraint


# class FuelSource(Base):

#     __tablename__ = "fuel_source"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30), unique=True)


# class VehicleType(Base):

#     __tablename__ = "vehicle_type"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30), unique=True)



class Car(Base):
    __tablename__ = "car"


    id: Mapped[int] = mapped_column(primary_key=True)

    make: Mapped[str] = mapped_column(String(32))
    model: Mapped[str] = mapped_column(String(128))
    sub_model: Mapped[str] = mapped_column(String(255))

    engines = relationship('Engine', back_populates='car')
    transmissions = relationship('Transmission', back_populates='car')
    hydraulic_brakes = relationship('HydraulicBrake', back_populates='car')
    power_steerings = relationship('PowerSteering', back_populates='car')
    cooling_systems = relationship('CoolingSystem', back_populates='car')


class Engine(Base):

    __tablename__ = "engine"

    id: Mapped[int] = mapped_column(primary_key=True)

    code:Mapped[str] = mapped_column(String(32), nullable=True)
    change_interval: Mapped[str] = mapped_column(String(255),  nullable=True)
    capacity: Mapped[str] = mapped_column(String(255),  nullable=True)
    viscosity: Mapped[str] = mapped_column(String(255),  nullable=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=True)
    car: Mapped["Car"] = relationship(back_populates="engines")

class Transmission(Base):
    
    __tablename__ = "transmission"

    id: Mapped[int] = mapped_column(primary_key=True)

    code:Mapped[str] = mapped_column(String(32), nullable=True)
    change_interval: Mapped[str] = mapped_column(String(255), nullable=True)
    capacity: Mapped[str] = mapped_column(String(255), nullable=True)
    viscosity: Mapped[str] = mapped_column(String(255), nullable=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    car: Mapped["Car"] = relationship(back_populates="transmissions")



class HydraulicBrake(Base):
    
    __tablename__ = "hydraulic_brake"

    id: Mapped[int] = mapped_column(primary_key=True)


    change_interval: Mapped[str] = mapped_column(String(32))
    check_interval: Mapped[str] = mapped_column(String(32))
    dot: Mapped[str] = mapped_column(String(128))

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    car: Mapped["Car"] = relationship(back_populates="hydraulic_brakes")


class PowerSteering(Base):
    
    __tablename__ = "power_steering"

    id: Mapped[int] = mapped_column(primary_key=True)


    change_interval: Mapped[str] = mapped_column(String(32))
    capacity: Mapped[str] = mapped_column(String(32))
    atf: Mapped[str] = mapped_column(String(128))

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    car: Mapped["Car"] = relationship(back_populates="power_steerings")


class CoolingSystem(Base):
    
    __tablename__ = "cooling_system"

    id: Mapped[int] = mapped_column(primary_key=True)

    change_interval: Mapped[str] = mapped_column(String(32))
    capacity: Mapped[str] = mapped_column(String(32))

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"))
    car: Mapped["Car"] = relationship(back_populates="cooling_systems")


