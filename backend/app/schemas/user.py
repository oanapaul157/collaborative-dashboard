from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=255)
    name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    name: str | None = Field(min_length=2, max_length=100)
    email: EmailStr | None = Field(max_length=255)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    created_at: datetime