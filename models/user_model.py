# File path: my_api/models/user_model.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    # Establishing the relationship with TodoList
    #todo_lists = relationship('TodoList', back_populates='user')

    def __repr__(self):
        return f"<User(username='{self.username}')>"