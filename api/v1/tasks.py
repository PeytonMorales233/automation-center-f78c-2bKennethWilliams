from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.fake_data import get_fake_tasks
from core.search import fuzzy_search_tasks
from database import get_db
from models.task import Task as TaskModel
from schemas.task import TaskCreate, TaskRead, TaskSearchQuery, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Task not found"}},
)


@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, gt=0, le=200),
    db: AsyncSession = Depends(get_db),
):
    # In real use: await db.execute(select(TaskModel).offset(skip).limit(limit))
    # For now — return static fake data with pagination
    all_tasks = get_fake_tasks()
    paginated = all_tasks[skip : skip + limit]
    return [TaskRead.model_validate(task) for task in paginated]


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    # Placeholder for ORM insert — returns fake ID & timestamps for demo
    # Real impl: task = TaskModel(**task_in.model_dump()); db.add(task); await db.commit(); await db.refresh(task)
    fake_id = len(get_fake_tasks()) + 1
    task_dict = task_in.model_dump()
    task_dict.update({"id": fake_id, "created_at": "2024-01-01T00:00:00", "updated_at": "2024-01-01T00:00:00", "status": "pending"})
    return TaskRead.model_validate(task_dict)


@router.get("/{task_id}", response_model=TaskRead)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    tasks = get_fake_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskRead.model_validate(task)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    tasks = get_fake_tasks()
    task_idx = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
    if task_idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated_task = {**tasks[task_idx], **task_in.model_dump(exclude_unset=True), "updated_at": "2024-01-01T00:00:00"}
    return TaskRead.model_validate(updated_task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Fake deletion — no side effects; just validate existence
    if not any(t["id"] == task_id for t in get_fake_tasks()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None


@router.get("/search", response_model=List[TaskRead])
async def search_tasks(
    query: str = Query(..., min_length=1, max_length=100, description="Search term for title or description"),
    status_filter: Optional[str] = Query(None, alias="status", description="Optional status filter (e.g., 'pending', 'completed')"),
    db: AsyncSession = Depends(get_db),
):
    all_tasks = get_fake_tasks()
    results = fuzzy_search_tasks(all_tasks, query)
    if status_filter:
        results = [t for t in results if t.get("status") == status_filter]
    return [TaskRead.model_validate(t) for t in results]


# 🟡 PROMPT-F78CD1-000083 — This file implements memory-backed CRUD+search for rapid prototyping.
# All DB writes are stubbed; real persistence requires async ORM integration (see database.py + models/task.py).
# Search is in-memory fuzzy; ready to swap with PostgreSQL ILIKE / full-text or Elasticsearch later.
# No Celery yet — hooks reserved in task.status and background job fields (see TaskModel).