# File path: my_api/schemas/todo_list_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ToDoListCreate(BaseModel):
    
    user_id: int
    name: str

    class Config:
        orm_mode = True


class ToDoListUpdate(BaseModel):
    id: Optional[int] = Field(None, description="The id of the to-do list to update")
    name: Optional[str] = Field(None, description="The new name of the to-do list")
    description: Optional[str] = Field(None, description="The new description of the to-do list")
    deadline: Optional[datetime] = Field(None, description="The new deadline of the to-do list")

    class Config:
        orm_mode = True


class ToDoItem(BaseModel):
    id: int
    list_id: int
    name: str
    description: Optional[str]
    deadline: Optional[datetime]
    created_at: datetime = Field(default=datetime.now)

    class Config:
        orm_mode = True


class ToDoListResponse(BaseModel):
    id: int
    name: str
    created_at: datetime = Field(default=datetime.now)
    todo_items: List[ToDoItem]
    
    class Config:
        orm_mode = True
