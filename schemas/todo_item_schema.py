# File path: my_api/schemas/todo_item_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schemas for To-Do items

class ToDoItemCreate(BaseModel):
    list_id: int
    name: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "list_id": 1,
                "name": "Go shopping",
                "description": "Need to get groceries and household items.",
                "deadline": "2023-12-31T23:59:59"
            }
        }


class ToDoItemUpdate(BaseModel):
    name: Optional[str] = Field(None, description='The new name of the ToDo item')
    description: Optional[str] = Field(None, description='The new description of the ToDo item')
    deadline: Optional[datetime] = Field(None, description='The new deadline for the ToDo item')


class ToDoItemResponse(BaseModel):
    id: int
    list_id: int
    name: str
    description: Optional[str] = Field(None, description='The description of the to-do item')
    deadline: Optional[datetime] = Field(None, description='The deadline for the to-do item')
    created_at: datetime = Field(default_factory=datetime.now, description='The time when the to-do item was created')

    class Config:
        orm_mode = True

    def __str__(self):
        return f'ToDoItemResponse(id={self.id}, list_id={self.list_id}, name={self.name}, description={self.description}, deadline={self.deadline}, created_at={self.created_at})'