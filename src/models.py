from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String, default='new')

class Responses(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String, default='pending')

