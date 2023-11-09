
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, make_transient
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import desc, asc

# 創建一個連接
engine = create_engine('mysql+pymysql://root:carletcarlet@127.0.0.1:3306/carlet')

# 創建一個基礎模型類
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


from . import models
