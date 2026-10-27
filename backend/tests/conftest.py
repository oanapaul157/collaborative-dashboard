import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base, get_db
from app.main import app
from app.models import (  # also imports the models, so Base.metadata knows every table
    Board,
    BoardMember,
    Column,
    Task,
    User,
)

TEST_DATABASE_URL = (
    "postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard_test"
)


@pytest.fixture(scope="session")
def engine():
    # Runs once for the whole test run: create the tables, drop them at the end
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db(engine):
    # Runs once per test: everything happens inside one transaction that gets rolled back.
    # "create_savepoint" turns your routers' db.commit() into a savepoint, so the rollback still undoes it.
    with engine.connect() as conn:
        outer = conn.begin()
        session = Session(
            bind=conn, join_transaction_mode="create_savepoint", expire_on_commit=False
        )
        yield session
        session.close()
        outer.rollback()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def user(db):
    user = User(
        email="test@exmaple.com", name="Test User", password_hash="not-a-real-hash"
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture
def other_user(db):
    user = User(
        email="test_other@exmaple.com",
        name="Other Test User",
        password_hash="not-a-real-hash",
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture
def auth_headers(user):
    return {"X-User-Id": str(user.id)}


@pytest.fixture
def board(db, user):
    board = Board(name="Test Board", owner=user)
    board.members.append(BoardMember(user=user, role="owner"))
    db.add(board)
    db.flush()
    return board


@pytest.fixture
def column(db, board):
    column = Column(name="Test Column", board=board, position=0)
    db.add(column)
    db.flush()
    return column


@pytest.fixture
def task(db, column):
    task = Task(title="Test Task", column=column, position=0)
    db.add(task)
    db.flush()
    return task
