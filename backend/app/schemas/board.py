from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.column import ColumnWithTasks


class BoardCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class BoardUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class BoardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    owner_id: int
    created_at: datetime


class BoardDetail(BoardRead):
    columns: list[ColumnWithTasks]
