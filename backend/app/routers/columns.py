from fastapi import APIRouter
from sqlalchemy import func, select

from app.deps import BoardDep, CurrentUser, DbSession, ColumnDep
from app.models import Column
from app.schemas.column import ColumnCreate, ColumnRead, ColumnUpdate


router = APIRouter(tags=["columns"])


@router.post("/boards/{board_id}/columns", response_model=ColumnRead, status_code=201)
def create_column(
    data: ColumnCreate,
    board: BoardDep,
    db: DbSession,
    user: CurrentUser
):
    stmt = select(func.max(Column.position)).where(Column.board_id == board.id)
    max_position = db.scalar(stmt)
    next_position = 0 if max_position is None else max_position + 1
    column = Column(name=data.name, position=next_position, board=board)
    db.add(column)
    db.commit()
    return column


@router.patch("/columns/{column_id}", response_model=ColumnRead)
def update_column(
    data: ColumnUpdate,
    db: DbSession,
    user: CurrentUser,
    column: ColumnDep
):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(column, field, value)
    db.commit()
    return column


@router.delete("/columns/{column_id}", status_code=204)
def delete_column(
    db: DbSession,
    user: CurrentUser,
    column: ColumnDep
):
    db.delete(column)
    db.commit()


@router.get("/columns/{column_id}", response_model=ColumnRead)
def get_column(
    user: CurrentUser,
    column: ColumnDep
):
    return column

