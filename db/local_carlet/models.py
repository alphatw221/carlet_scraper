from typing import List

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Index, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, INTEGER, TINYINT, VARCHAR, YEAR, FLOAT
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

from . import Base
# Base = declarative_base()


class VehicleDefCountry(Base):
    __tablename__ = 'vehicle_def_country'
    __table_args__ = (
        Index('country', 'country', unique=True),
        {'comment': '車系定義'}
    )

    id = mapped_column(BIGINT, primary_key=True, comment='pk')
    country = mapped_column(CHAR(8), nullable=False, comment='車系')
    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    vehicle_model: Mapped[List['VehicleModel']] = relationship('VehicleModel', uselist=True, back_populates='vehicle_def_country')


class VehicleMake(Base):
    __tablename__ = 'vehicle_make'
    __table_args__ = (
        Index('name', 'name', unique=True),
        {'comment': 'vehicle manufacturer'}
    )

    id = mapped_column(BIGINT, primary_key=True, comment='pk')
    name = mapped_column(VARCHAR(64), nullable=False, comment='manufacturer')
    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    vehicle_model: Mapped[List['VehicleModel']] = relationship('VehicleModel', uselist=True, back_populates='make')


class VehicleModel(Base):
    __tablename__ = 'vehicle_model'
    __table_args__ = (
        ForeignKeyConstraint(['country'], ['vehicle_def_country.country'], onupdate='CASCADE', name='vehicle_model_ibfk_2'),
        ForeignKeyConstraint(['make_id'], ['vehicle_make.id'], onupdate='CASCADE', name='vehicle_model_ibfk_1'),
        Index('country', 'country'),
        Index('unique', 'make_id', 'year', 'displacement', 'fuel', 'transmission', 'trim_level', 'name', 'variant', unique=True),
        {'comment': 'vehicle models'}
    )

    id = mapped_column(BIGINT, primary_key=True, comment='pk')
    make_id = mapped_column(BIGINT, nullable=False, comment='品牌id, fk vehicle_make.id')
    year = mapped_column(YEAR, nullable=False, comment='年份, fk vehicle_make.year')
    name = mapped_column(VARCHAR(64), nullable=False, comment='型號, model name')
    variant = mapped_column(VARCHAR(64), nullable=False, server_default=text("''"), comment='款式, model variant')
    name_variant = mapped_column(VARCHAR(192), nullable=False, comment='型號款式, model name and variant and trim_level')
    displacement = mapped_column(INTEGER, nullable=False, comment='排氣量, engine displacement')
    fuel = mapped_column(CHAR(16), nullable=False, comment='燃料, engine type, fuel type')
    transmission = mapped_column(CHAR(16), nullable=False, comment='變速箱, multi-speed transmission')
    trim_level = mapped_column(VARCHAR(64), nullable=False, server_default=text("''"), comment='車型, model trim level')
    code = mapped_column(VARCHAR(64), nullable=False, server_default=text("''"), comment='車型代號, body code/vin')
    size = mapped_column(CHAR(16), nullable=False, comment='大小, vehicle body size')
    country = mapped_column(CHAR(8), nullable=False, server_default=text("'未定'"), comment='車系(無使用, 來源沒有)')
    supported = mapped_column(TINYINT, nullable=False, comment='開放,do we support maintenance')
    is_show = mapped_column(TINYINT, nullable=False, server_default=text("'0'"), comment='是否在前端顯示')
    engine = mapped_column(CHAR(192), nullable=False, server_default=text("''"), comment='引擎代號')
    chassis = mapped_column(CHAR(192), nullable=False, server_default=text("''"), comment='底盤代號')
    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    hash1 = mapped_column(CHAR(32), nullable=False, server_default=text("''"), comment='temporary using')
    hash2 = mapped_column(CHAR(32), nullable=False, server_default=text("''"), comment='temporary using')
    deleted_ts = mapped_column(BIGINT, server_default=text("'0'"), comment="unixtime, we won't really delete accounts")


    output =  mapped_column(CHAR(16), nullable=True, comment='輸出')
    vehicle_def_country: Mapped['VehicleDefCountry'] = relationship('VehicleDefCountry', back_populates='vehicle_model')
    make: Mapped['VehicleMake'] = relationship('VehicleMake', back_populates='vehicle_model')


    auto_data_id = mapped_column(BIGINT, nullable=True, comment='Auto Data ID')
    tire_rack_id = mapped_column(BIGINT, nullable=True, comment='Tire Rack ID')

class Vehicle(Base):

    __tablename__ = 'vehicle'
    

    id = mapped_column(BIGINT, primary_key=True, comment='pk')

    # make_id = mapped_column(BIGINT, nullable=False, comment='品牌id, fk vehicle_make.id')



    # year = mapped_column(YEAR, nullable=False, comment='年份')
    make = mapped_column(VARCHAR(64), nullable=False, comment='車廠')
    model = mapped_column(VARCHAR(128), nullable=False, comment='型號')
    sub_model = mapped_column(VARCHAR(255), nullable=False, comment='子型號')
    
    price = mapped_column(FLOAT, nullable=False, server_default=text('0'), comment='售價')
    output = mapped_column(VARCHAR(128), nullable=False, server_default='', comment='子型號')
    displacement = mapped_column(VARCHAR(128), nullable=False, server_default='', comment='排氣量')

    created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


    # displacement = mapped_column(INTEGER, nullable=False, comment='排氣量, engine displacement')
    # fuel = mapped_column(CHAR(16), nullable=False, comment='燃料, engine type, fuel type')
    # transmission = mapped_column(CHAR(16), nullable=False, comment='變速箱, multi-speed transmission')
    # trim_level = mapped_column(VARCHAR(64), nullable=False, server_default=text("''"), comment='車型, model trim level')
    # code = mapped_column(VARCHAR(64), nullable=False, server_default=text("''"), comment='車型代號, body code/vin')
    # size = mapped_column(CHAR(16), nullable=False, comment='大小, vehicle body size')
    # country = mapped_column(CHAR(8), nullable=False, server_default=text("'未定'"), comment='車系(無使用, 來源沒有)')
    # supported = mapped_column(TINYINT, nullable=False, comment='開放,do we support maintenance')
    # is_show = mapped_column(TINYINT, nullable=False, server_default=text("'0'"), comment='是否在前端顯示')
    # engine = mapped_column(CHAR(192), nullable=False, server_default=text("''"), comment='引擎代號')
    # chassis = mapped_column(CHAR(192), nullable=False, server_default=text("''"), comment='底盤代號')
    # created_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    # updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    # hash1 = mapped_column(CHAR(32), nullable=False, server_default=text("''"), comment='temporary using')
    # hash2 = mapped_column(CHAR(32), nullable=False, server_default=text("''"), comment='temporary using')
    # deleted_ts = mapped_column(BIGINT, server_default=text("'0'"), comment="unixtime, we won't really delete accounts")

    # vehicle_def_country: Mapped['VehicleDefCountry'] = relationship('VehicleDefCountry', back_populates='vehicle_model')
    # make: Mapped['VehicleMake'] = relationship('VehicleMake', back_populates='vehicle_model')
