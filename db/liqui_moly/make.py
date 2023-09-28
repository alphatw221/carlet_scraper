# from . import Base, engine



# from typing import List
# from typing import Optional
# from sqlalchemy import ForeignKey
# from sqlalchemy import String, Uuid, Date, Integer
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship

# from sqlalchemy import UniqueConstraint



# class Make(Base):

#     __tablename__ = "make"


#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(64), unique=True)


#     cars: Mapped[List["Car"]] = relationship(
#         back_populates="make", cascade="all, delete-orphan"
#     )

