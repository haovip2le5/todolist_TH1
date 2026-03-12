from typing import List, Optional, Tuple
from app.repositories.todo import TodoRepository
from app.models.todo import TodoModel


class TodoService:
    """Service quản lý logic Todo"""
    
    def __init__(self, repo: TodoRepository):
        self.repo = repo
    
    def create_todo(self, owner_id: int, title: str, description: Optional[str] = None, is_done: bool = False) -> TodoModel:
        """Tạo todo"""
        return self.repo.create(owner_id, title, description, is_done)
    
    def get_todos(
        self,
        owner_id: int,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[TodoModel], int]:
        """Lấy danh sách todos của user"""
        return self.repo.get_paginated(owner_id, is_done, q, sort, limit, offset)
    
    def get_todo_by_id(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Lấy todo theo id"""
        return self.repo.get_by_id(todo_id, owner_id)
    
    def update_todo(self, todo_id: int, owner_id: int, title: str, description: Optional[str], is_done: bool) -> Optional[TodoModel]:
        """Cập nhật toàn bộ todo"""
        return self.repo.update(todo_id, owner_id, title, description, is_done)
    
    def partial_update_todo(self, todo_id: int, owner_id: int, **kwargs) -> Optional[TodoModel]:
        """Cập nhật một phần todo"""
        return self.repo.partial_update(todo_id, owner_id, **kwargs)
    
    def delete_todo(self, todo_id: int, owner_id: int) -> bool:
        """Xóa todo"""
        return self.repo.delete(todo_id, owner_id)
    
    def complete_todo(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Đánh dấu todo hoàn thành"""
        return self.repo.partial_update(todo_id, owner_id, is_done=True)
