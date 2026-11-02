from typing import Literal

from fastapi import APIRouter, Query

from schemas import TaskCreate

from services.task_service import (
    create_task_service,
    get_tasks_service,
    get_task_service,
    update_task_service,
    delete_task_service
)

# Create a router
router = APIRouter()


# Create a new task
@router.post("/tasks")
def create_task(task: TaskCreate):
    return create_task_service(task)


# Get tasks with pagination and filtering
@router.get("/tasks")
def get_tasks(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status: Literal["pending", "in progress", "completed"] | None = None,
    priority: Literal["low", "medium", "high"] | None = None
):
    return get_tasks_service(
        limit,
        offset,
        status,
        priority
    )


# Get one task by ID
@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    return get_task_service(task_id)


# Update a task
@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    return update_task_service(task_id, task)


# Delete a task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return delete_task_service(task_id)