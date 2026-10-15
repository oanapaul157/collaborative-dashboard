from collections.abc import Iterator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# The engine owns a pool of connections to Postgres. Create it once per app.
# echo=True logs every SQL statement, handy while learning; turn it off later.
engine = create_engine(settings.database_url, echo=True)

# A factory for Sessions. A Session is a "unit of work": it tracks the objects
# you load/add and turns them into INSERT/UPDATE/DELETE when you commit.
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

# Gives every constraint a predictable name (e.g. "fk_tasks_column_id_columns").
# Without this, Postgres invents names, and Alembic can't reliably drop or
# alter those constraints in later migrations.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Parent class of every model. Its `metadata` collects all tables,
    which is what Alembic compares against the real DB to autogenerate migrations."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def get_db() -> Iterator[Session]:
    """FastAPI dependency: one Session per request, always closed afterwards.

    Used in step 2 as `db: Session = Depends(get_db)`. Code before `yield` runs
    before the endpoint, code after it runs once the response is done.
    """
    with SessionLocal() as session:
        yield session
