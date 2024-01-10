# File path: my_api/models/todo_item_model.py
import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class ToDoItem(Base):
    __tablename__ = 'todo_items'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    list_id = Column(Integer, ForeignKey('todo_lists.id', ondelete='CASCADE'))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    deadline = Column(DateTime)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    # Relationship to access the ToDoList this item is associated with
    todo_list = relationship('ToDoList', back_populates='todo_items')

    def __repr__(self):
        return f"<ToDoItem name={self.name} list_id={self.list_id}>"
