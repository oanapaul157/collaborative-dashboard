from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskUpdate(BaseModel):
    title: str | None = Field(min_length=1, max_length=200)
    description: str | None = Field(max_length=5000)


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    column_id: int
    title: str
    description: str | None
    position: int
    created_at: datetime
