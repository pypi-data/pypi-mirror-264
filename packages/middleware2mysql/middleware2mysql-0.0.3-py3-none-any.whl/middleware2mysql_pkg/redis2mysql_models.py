from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String,JSON,Integer,DateTime

Base = declarative_base()

class StringData(Base):
    __tablename__ = 'string_data'
    id = Column(Integer,primary_key=True,autoincrement=True)
    key = Column(String(255))
    value = Column(String(255))
    expiretime = Column(DateTime)


class HashData(Base):
    __tablename__ = 'hash_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255))
    field = Column(String(255))
    value = Column(JSON)

