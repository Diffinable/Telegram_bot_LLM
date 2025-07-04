from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

def save_messages(chat_id: str, user_id: int, text: str) -> int:
    conn = sqlite3.connect('data/db.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (chat_id, user_id, text, status) VALUES (?, ?, ?, ?)',
        (chat_id, user_id, text, "new")
    )
    message_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return message_id

