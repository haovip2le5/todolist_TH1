from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.todo import (
    TodoCreate, TodoUpdate, TodoPartialUpdate, Todo, TodoListResponse
)
from app.repositories.todo import TodoRepository
from app.services.todo import TodoService
from app.core.database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])


# Dependency to create service
def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    repo = TodoRepository(db)
    return TodoService(repo)


@router.post("", response_model=Todo)
def create_todo(todo: TodoCreate, service: TodoService = Depends(get_todo_service)):
    """Tạo todo mới"""
    return service.create_todo(todo.title, todo.description, todo.is_done)


@router.get("", response_model=TodoListResponse)
def get_todos(
    is_done: Optional[bool] = Query(None, description="Filter by is_done"),
    q: Optional[str] = Query(None, description="Search by title"),
    sort: Optional[str] = Query(None, description="Sort by: created_at, -created_at, title, -title"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: TodoService = Depends(get_todo_service)
):
    """Lấy danh sách todos"""
    items, total = service.get_todos(is_done, q, sort, limit, offset)
    return TodoListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    """Lấy chi tiết todo"""
    todo = service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return todo


@router.put("/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    service: TodoService = Depends(get_todo_service)
):
    """Cập nhật toàn bộ todo"""
    todo = service.update_todo(todo_id, todo_data.title, todo_data.description, todo_data.is_done)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return todo


@router.patch("/{todo_id}", response_model=Todo)
def partial_update_todo(
    todo_id: int,
    todo_data: TodoPartialUpdate,
    service: TodoService = Depends(get_todo_service)
):
    """Cập nhật một phần todo"""
    update_data = todo_data.model_dump(exclude_unset=True)
    todo = service.partial_update_todo(todo_id, **update_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return todo


@router.post("/{todo_id}/complete", response_model=Todo)
def complete_todo(
    todo_id: int,
    service: TodoService = Depends(get_todo_service)
):
    """Đánh dấu todo hoàn thành"""
    todo = service.complete_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    """Xóa todo"""
    if not service.delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return {"message": "Xóa thành công", "id": todo_id}
