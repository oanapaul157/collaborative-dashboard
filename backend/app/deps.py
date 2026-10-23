from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Board, Column, Task, User

DbSession = Annotated[Session, Depends(get_db)]


# Placeholder until real authentication is added
def get_current_user(x_user_id: Annotated[int, Header()], db: DbSession) -> User:
    user = db.get(User, x_user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Unknown User")
    return user


def get_board_or_404(board_id: int, db: DbSession) -> Board:
    board = db.get(Board, board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


def get_column_or_404(column_id: int, db: DbSession) -> Column:
    column = db.get(Column, column_id)
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return column


def get_task_or_404(task_id: int, db: DbSession) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


CurrentUser = Annotated[User, Depends(get_current_user)]
BoardDep = Annotated[Board, Depends(get_board_or_404)]
ColumnDep = Annotated[Column, Depends(get_column_or_404)]
TaskDep = Annotated[Task, Depends(get_task_or_404)]
