from pydantic import BaseModel


class StudentCreate(BaseModel):
    legajo: str
    carrera: str
    anio_ingreso: int


class StudentUpdate(BaseModel):
    carrera: str | None = None
    anio_ingreso: int | None = None


class StudentResponse(BaseModel):
    id: int
    user_id: int
    legajo: str
    carrera: str
    anio_ingreso: int

    class Config:
        from_attributes = True