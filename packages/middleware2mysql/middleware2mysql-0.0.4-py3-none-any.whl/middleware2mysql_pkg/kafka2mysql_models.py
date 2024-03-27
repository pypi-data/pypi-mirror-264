from datetime import datetime
from sqlalchemy import JSON, Column, Integer, String, UniqueConstraint,DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Message(Base):
    __tablename__ = 'kafka_data'
    id = Column(Integer, primary_key=True)
    topic = Column(String(255))
    message = Column(JSON)
    create_time = Column(DateTime, default=datetime.now, nullable=False, comment='创建时间')

class MessageFlag(Base):
    __tablename__ = 'kafka_flag_data'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    group_id = Column(String(32))
    flag = Column(Integer, default=0)
    __table_args__ = (
        UniqueConstraint('message_id', 'group_id', name='_message_group_uc'),
    )
