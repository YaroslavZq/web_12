from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    favorite = Column(Boolean, default=False)
    phone = Column(String(12), default="")
