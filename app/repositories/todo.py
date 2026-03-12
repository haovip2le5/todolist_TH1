from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.todo import TodoModel


class TodoRepository:
    """Repository quản lý dữ liệu Todo từ Database"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, owner_id: int, title: str, description: Optional[str] = None, is_done: bool = False) -> TodoModel:
        """Tạo todo mới"""
        todo = TodoModel(owner_id=owner_id, title=title, description=description, is_done=is_done)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def get_by_id(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Lấy todo theo id (chỉ của user hiện tại)"""
        return self.db.query(TodoModel).filter(
            TodoModel.id == todo_id,
            TodoModel.owner_id == owner_id
        ).first()
    
    def get_all_by_owner(self, owner_id: int) -> List[TodoModel]:
        """Lấy tất cả todos của user"""
        return self.db.query(TodoModel).filter(TodoModel.owner_id == owner_id).all()
    
    def update(self, todo_id: int, owner_id: int, title: str, description: Optional[str], is_done: bool) -> Optional[TodoModel]:
        """Cập nhật toàn bộ todo"""
        todo = self.get_by_id(todo_id, owner_id)
        if not todo:
            return None
        todo.title = title
        todo.description = description
        todo.is_done = is_done
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def partial_update(self, todo_id: int, owner_id: int, **kwargs) -> Optional[TodoModel]:
        """Cập nhật một phần todo"""
        todo = self.get_by_id(todo_id, owner_id)
        if not todo:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(todo, key):
                setattr(todo, key, value)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    
    def delete(self, todo_id: int, owner_id: int) -> bool:
        """Xóa todo"""
        todo = self.get_by_id(todo_id, owner_id)
        if not todo:
            return False
        self.db.delete(todo)
        self.db.commit()
        return True
    
    def get_paginated(
        self,
        owner_id: int,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[TodoModel], int]:
        """Lấy todos với filter, search, sort, pagination từ DB"""
        query = self.db.query(TodoModel).filter(TodoModel.owner_id == owner_id)
        
        # Filter by is_done
        if is_done is not None:
            query = query.filter(TodoModel.is_done == is_done)
        
        # Search by title
        if q:
            query = query.filter(TodoModel.title.ilike(f"%{q}%"))
        
        # Get total before pagination
        total = query.count()
        
        # Sort
        if sort:
            reverse = sort.startswith("-")
            sort_key = sort.lstrip("-") or "created_at"
            if sort_key == "created_at":
                query = query.order_by(desc(TodoModel.created_at) if reverse else TodoModel.created_at)
            elif sort_key == "title":
                query = query.order_by(desc(TodoModel.title) if reverse else TodoModel.title)
        
        # Pagination
        items = query.offset(offset).limit(limit).all()
        
        return items, total
