
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
# 創建一個連接
engine = create_engine('postgresql+psycopg2://postgres:kp80390254tnt0221!!@18.136.209.77/carlet')

# 創建一個基礎模型類
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


from . import car
