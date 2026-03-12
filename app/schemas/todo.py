from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class TodoCreate(BaseModel):
    """Schema tạo todo"""
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    is_done: bool = False


class TodoUpdate(BaseModel):
    """Schema cập nhật toàn bộ todo"""
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    is_done: bool


class TodoPartialUpdate(BaseModel):
    """Schema cập nhật một phần todo"""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    is_done: Optional[bool] = None


class Todo(BaseModel):
    """Schema todo"""
    id: int
    title: str
    description: Optional[str]
    is_done: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """Schema response danh sách todo"""
    items: List[Todo]
    total: int
    limit: int
    offset: int
