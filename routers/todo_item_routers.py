# File path: my_api/routers/todo_item_routers.py
import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Any
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
from models.todo_item_model import ToDoItem
from schemas.todo_item_schema import ToDoItemCreate, ToDoItemResponse, ToDoItemUpdate
from database import Base

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/todo-items")


@router.post("/", response_model=ToDoItemResponse)
def create_todo_item(item: ToDoItemCreate, db: Session = Depends(get_db)):
    new_item = ToDoItem(
        list_id=item.list_id,
        name=item.name,
        description=item.description,
        deadline=item.deadline
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/todo-items/{item_id}", response_model=ToDoItemResponse)
def get_todo_item(item_id: int = Path(..., description="The ID of the ToDoItem to retrieve"), db: Session = Depends(get_db)) -> Any:
  todo_item = db.query(ToDoItem).filter(ToDoItem.id == item_id).first()

  if todo_item is None:
    raise HTTPException(status_code=404, detail="ToDoItem not found")

  return todo_item


@router.get('/todo-items/', response_model=List[ToDoItemResponse])
def get_todo_items(db: Session = Depends(get_db)):
    todo_items = db.query(ToDoItem).all()
    return todo_items


@router.put("/todo-items/{item_id}", response_model=ToDoItemResponse)
def update_todo_item(
    *,
    db: Session = Depends(get_db),
    item_id: int = Path(..., description="The ID of the ToDoItem to update"),
    todo_item_update: ToDoItemUpdate
) -> Any:
    todo_item = db.query(ToDoItem).filter(ToDoItem.id == item_id).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="ToDoItem not found")

    update_data = todo_item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo_item, key, value)

    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)

    return todo_item


@router.delete("/todo-items/{item_id}", response_model=str)
def delete_todo_item(item_id: int = Path(..., description="The ID of the todo item to delete"), db: Session = Depends(get_db)):
    todo_item = db.query(ToDoItem).filter(ToDoItem.id == item_id).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="ToDoItem not found")
    db.delete(todo_item)
    db.commit()
    return f"ToDoItem with ID {item_id} successfully deleted"


@router.get('/search-items/', response_model=List[ToDoItemResponse], summary="Search ToDoItems based on query parameters")
async def search_todo_items(
    query_params: str = Query(None, title="Query Parameters", description="Query parameters to search todo items"),
    db: Session = Depends(get_db)
):
    search_query = "%" + query_params + "%"
    todo_items = db.query(ToDoItem).filter(
        ToDoItem.name.like(search_query) |
        ToDoItem.description.like(search_query)
    ).all()

    if not todo_items:
        raise HTTPException(status_code=404, detail="ToDoItems not found")

    return todo_items
