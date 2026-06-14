from pydantic import BaseModel
from datetime import datetime


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True