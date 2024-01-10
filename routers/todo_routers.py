# File path: my_api/routers/todo_routers.py
from fastapi import APIRouter, HTTPException, Depends, status, Path, Query, Body
from typing import List, Any, Union
from sqlalchemy.orm import Session

from models.todo_model import ToDoList
from models.todo_item_model import ToDoItem
from schemas.todo_list_schema import ToDoListCreate, ToDoListResponse, ToDoListUpdate
from schemas.todo_item_schema import ToDoItemCreate, ToDoItemResponse, ToDoItemUpdate
from database import get_db, Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post('/todo-lists/', response_model=ToDoListResponse, status_code=status.HTTP_201_CREATED)
def create_todo_list(todo_list_create: ToDoListCreate, db: Session = Depends(get_db)):
    new_todo_list = ToDoList(
        user_id=todo_list_create.user_id,
        name=todo_list_create.name
    )
    db.add(new_todo_list)
    db.commit()
    db.refresh(new_todo_list)
    return new_todo_list

@router.get('/todo-lists/', response_model=List[ToDoListResponse])
def get_todo_lists(user_id: int, db: Session = Depends(get_db)):
    todo_lists = db.query(ToDoList).filter(ToDoList.user_id == user_id).all()
    if not todo_lists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No to-do lists found for the user.")
    return todo_lists

@router.get('/todo-lists/{list_id}', response_model=ToDoListResponse)
def get_todo_list(
        list_id: int,
        db: Session = Depends(get_db)
    ):
    todo_list = db.query(ToDoList).filter(ToDoList.id == list_id).first()
    if not todo_list:
        raise HTTPException(status_code=404, detail="ToDo list not found")
    return todo_list

@router.put('/todo-lists/{list_id}', response_model=ToDoListResponse)
def update_todo_list(
        list_id: int,
        todo_list_update: ToDoListUpdate = Body(...),
        db: Session = Depends(get_db)
):
    todo_list = db.query(ToDoList).filter(ToDoList.id == list_id).first()
    if not todo_list:
        raise HTTPException(status_code=404, detail="To-do list not found")

    update_data = todo_list_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo_list, key, value)

    db.add(todo_list)
    db.commit()
    db.refresh(todo_list)
    return todo_list

@router.delete('/todo-lists/{list_id}', response_model=str)
def delete_todo_list(
    list_id: int = Path(..., description="The ID of the to-do list to delete"),
    db: Session = Depends(get_db)
    ):
    todo_list = db.query(ToDoList).filter(ToDoList.id == list_id).first()
    if not todo_list:
        raise HTTPException(status_code=404, detail="To-do list not found")
    db.delete(todo_list)
    db.commit()
    return f"Successfully deleted to-do list with id {list_id}"

@router.post("/todo-lists/{list_id}/items/", response_model=ToDoItemResponse, status_code=status.HTTP_201_CREATED)
def create_todo_item(
    *,
    list_id: int,
    todo_item_create: ToDoItemCreate,
    db: Session = Depends(get_db)
):
    todo_list = db.query(ToDoList).filter(ToDoList.id == list_id).first()
    if not todo_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The to-do list does not exist."
        )

    todo_item = ToDoItem(**todo_item_create.dict())
    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)

    return todo_item

@router.get("/todo-lists/{list_id}/items/{item_id}", response_model=ToDoItemResponse)
def get_todo_item(
        list_id: int = Path(..., description="The ID of the to-do list", gt=0),
        item_id: int = Path(..., description="The ID of the to-do item", gt=0),
        db: Session = Depends(get_db)
    ):
    todo_item = db.query(models.ToDoItem).filter(models.ToDoItem.id == item_id, models.ToDoItem.list_id == list_id).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return todo_item

@router.get('/todo-lists/{list_id}/items/', response_model=List[ToDoItemResponse])
def get_todo_items(list_id: int, db: Session = Depends(get_db)):
    todo_list = db.query(ToDoList).filter(ToDoList.id == list_id).first()
    if not todo_list:
        raise HTTPException(status_code=404, detail="To-do list not found")
    items = db.query(ToDoItem).filter(ToDoItem.list_id == list_id).all()
    return items

@router.put("/todo-lists/{list_id}/items/{item_id}", response_model=ToDoItemResponse)
def update_todo_item(
        list_id: int,
        item_id: int,
        todo_item_update: ToDoItemUpdate,
        db: Session = Depends(get_db),
) -> Any:
    todo_item = db.query(models.ToDoItem).filter(models.ToDoItem.id == item_id,
                                                        models.ToDoItem.list_id == list_id).first()
    if not todo_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} and list_id {list_id} not found",
        )

    update_data = todo_item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo_item, key, value)

    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)

    return todo_item

@router.delete('/todo-lists/{list_id}/items/{item_id}', response_model=str)
def delete_todo_item(
        list_id: int = Path(..., description="The id of the to-do list"),
        item_id: int = Path(..., description="The id of the to-do item"),
        db: Session = Depends(get_db)):
    item = db.query(models.ToDoItem).filter(models.ToDoItem.id == item_id, models.ToDoItem.list_id == list_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="To-do item not found")

    db.delete(item)
    db.commit()

    return "To-do item deleted successfully"

@router.get("/search", response_model=List[Union[ToDoListResponse, ToDoItemResponse]])
def search_todos(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    todo_lists = db.query(ToDoList).filter(ToDoList.name.ilike(f"%{query}%")).all()
    todo_items = db.query(ToDoItem).filter(ToDoItem.name.ilike(f"%{query}%")).all()

    if not todo_lists and not todo_items:
        raise HTTPException(status_code=404, detail="No matching to-do lists or items found.")

    combined_results = []
    for todo_list in todo_lists:
        combined_results.append(ToDoListResponse.from_orm(todo_list))
    for todo_item in todo_items:
        combined_results.append(ToDoItemResponse.from_orm(todo_item))

    return combined_results
