from pydantic import BaseModel, ConfigDict, Field

from app.schemas.task import TaskRead


class ColumnCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ColumnUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ColumnRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    board_id: int
    position: int


class ColumnWithTasks(ColumnRead):
    tasks: list[TaskRead]
