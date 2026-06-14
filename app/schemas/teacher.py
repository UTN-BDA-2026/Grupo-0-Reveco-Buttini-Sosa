from pydantic import BaseModel


class TeacherCreate(BaseModel):
    legajo: str
    departamento: str
    titulo: str


class TeacherUpdate(BaseModel):
    departamento: str | None = None
    titulo: str | None = None


class TeacherResponse(BaseModel):
    id: int
    user_id: int
    legajo: str
    departamento: str
    titulo: str

    class Config:
        from_attributes = True