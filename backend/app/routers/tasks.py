from fastapi import APIRouter
from sqlalchemy import func, select

from app.deps import CurrentUser, DbSession, ColumnDep, TaskDep
from app.models import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


router = APIRouter(tags=["tasks"])


@router.post("/columns/{column_id}/tasks", response_model=TaskRead, status_code=201)
def create_task(
    data: TaskCreate,
    column: ColumnDep,
    db: DbSession,
    user: CurrentUser
):
    stmt = select(func.max(Task.position)).where(Task.column_id == column.id)
    max_position = db.scalar(stmt)
    next_position = 0 if max_position is None else max_position + 1
    task = Task(title=data.title, position=next_position, column=column)
    db.add(task)
    db.commit()
    return task


@router.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    data: TaskUpdate,
    db: DbSession,
    user: CurrentUser,
    task: TaskDep
):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    db: DbSession,
    user: CurrentUser,
    task: TaskDep
):
    db.delete(task)
    db.commit()


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user: CurrentUser,
    task: TaskDep
):
    return task