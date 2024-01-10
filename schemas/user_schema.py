# File path: my_api/schemas/user_schema.py
from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(..., description='Unique username for the user.')
    password_hash: str = Field(..., description='Hash of the user password.')

    class Config:
        schema_extra = {
            'description': 'Schema to create a new user.'
        }


class UserUpdate(BaseModel):
    """Schema to update an existing user."""
    username: constr(strip_whitespace=True, min_length=1, max_length=255)
    password_hash: constr(strip_whitespace=True, min_length=1, max_length=255)


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True
