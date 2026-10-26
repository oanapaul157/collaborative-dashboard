from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

TaskTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
]


class TaskCreate(BaseModel):
    title: TaskTitle = Field(min_length=1, max_length=200)


class TaskUpdate(BaseModel):
    title: TaskTitle | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)

    @field_validator("title")
    @classmethod
    def title_not_null(cls, v: str | None) -> str | None:
        if v is None:
            raise ValueError("Title cannot be empty")
        return v


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    column_id: int
    title: str
    description: str | None
    position: int
    created_at: datetime
