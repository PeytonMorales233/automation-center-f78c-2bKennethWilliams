from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="任务标题")
    description: Optional[str] = Field(None, max_length=1000, description="任务描述")
    status: str = Field("pending", pattern="^(pending|running|completed|failed|cancelled)$", description="任务状态")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int = Field(..., ge=1, description="任务唯一标识")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="最后更新时间")

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, pattern="^(pending|running|completed|failed|cancelled)$")


class TaskSearchQuery(BaseModel):
    q: Optional[str] = Field(None, min_length=1, max_length=200, description="搜索关键词，模糊匹配 title 或 description")
    status: Optional[str] = Field(None, pattern="^(pending|running|completed|failed|cancelled)$", description="按状态筛选")
    offset: int = Field(0, ge=0, description="分页偏移量")
    limit: int = Field(20, ge=1, le=100, description="每页数量，上限 100")
