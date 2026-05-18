from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

