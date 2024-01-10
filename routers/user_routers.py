# File path: my_api/routers/user_routers.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from models.user_model import User
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from database import get_db

router = APIRouter(tags=["users"])

@router.post('/users/', response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')

    # Create new user instance
    new_user = User(username=user.username, password_hash=user.password_hash)

    # Add to the session and commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Convert to Pydantic model
    return new_user

@router.get('/users/{id}', response_model=UserResponse, summary="Get user by id")
async def get_user_by_id(
        id: int,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponse])
async def get_users(
    username: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if username:
        users = db.query(User).filter(User.username.ilike(f"%{username}%")).all()
    else:
        users = db.query(User).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    return users

@router.put('/users/{id}', response_model=UserResponse)
def update_user(
        id: int,
        user_update: UserUpdate,
        db: Session = Depends(get_db)
) -> Any:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    for var, value in vars(user_update).items():
        setattr(user, var, value) if value else None
    db.commit()
    db.refresh(user)
    return user

@router.delete('/users/{id}', response_model=dict)
def delete_user(id: int, db: Session = Depends(get_db)):
    # Retrieve the user by id
    user = db.query(User).filter(User.id == id).first()
    # If user is not found, raise HTTP 404 error
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Delete the user from the database
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
