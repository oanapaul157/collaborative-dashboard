from fastapi import APIRouter
from sqlalchemy import select

from app.models import Board, BoardMember
from app.schemas.board import BoardCreate, BoardRead, BoardUpdate
from app.deps import BoardDep, CurrentUser, DbSession


router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("", response_model=BoardRead, status_code=201)
def create_board(
    data: BoardCreate,
    db: DbSession,
    user: CurrentUser
):
    board = Board(name=data.name, owner=user)
    board.members.append(BoardMember(user=user, role="owner"))
    db.add(board)
    db.commit()
    return board


@router.get("", response_model=list[BoardRead])
def list_boards(db: DbSession, user: CurrentUser):
    stmt = (
        select(Board)
        .join(BoardMember)
        .where(BoardMember.user_id == user.id)
        .order_by(Board.created_at)
    )
    return db.scalars(stmt).all()


@router.patch("/{board_id}", response_model=BoardRead)
def update_board(
    data: BoardUpdate,
    db: DbSession,
    user: CurrentUser,
    board: BoardDep,
):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(board, field, value)
    db.commit()
    return board


@router.get("/{board_id}", response_model=BoardRead)
def get_board(user: CurrentUser, board: BoardDep):
    return board


@router.delete("/{board_id}", status_code=204)
def delete_board(user: CurrentUser, board: BoardDep, db: DbSession):
    db.delete(board)
    db.commit()