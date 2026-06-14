from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.schemas.role import RoleResponse


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str
    role_id: int          # Ahora es obligatorio al registrarse


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
    role: RoleResponse    # Devuelve el objeto role completo, no solo el id

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str