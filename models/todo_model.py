# File path: my_api/models/todo_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class ToDoList(Base):
    __tablename__ = 'todo_lists'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    # Relationships
    #user = relationship('User', back_populates='todo_lists')
    todo_items = relationship('ToDoItem', back_populates='todo_list', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<ToDoList(id={self.id}, name={self.name}), todo_items={self.todo_items}>"
