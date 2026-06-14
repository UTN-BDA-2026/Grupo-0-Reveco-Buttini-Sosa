from pydantic import BaseModel


class StaffCreate(BaseModel):
    legajo: str
    sector: str
    cargo: str


class StaffUpdate(BaseModel):
    sector: str | None = None
    cargo: str | None = None


class StaffResponse(BaseModel):
    id: int
    user_id: int
    legajo: str
    sector: str
    cargo: str

    class Config:
        from_attributes = True