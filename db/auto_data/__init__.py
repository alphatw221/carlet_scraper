
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, make_transient
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import desc, asc

# 創建一個連接
engine = create_engine('postgresql+psycopg2://postgres:kp80390254tnt0221!!@18.136.209.77/auto_data')

# 創建一個基礎模型類
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


from . import car
