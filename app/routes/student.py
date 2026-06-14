from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.student import StudentRepository
from app.services.student import StudentService
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    return StudentService(StudentRepository(db))


# Crear perfil de alumno
@router.post("/{user_id}", response_model=StudentResponse, status_code=201)
def create_student(
    user_id: int,
    student_data: StudentCreate,
    service: StudentService = Depends(get_student_service)
):
    return service.create_student(user_id, student_data)


# Obtener perfil de alumno por user_id
@router.get("/{user_id}", response_model=StudentResponse)
def get_student(
    user_id: int,
    service: StudentService = Depends(get_student_service)
):
    return service.get_by_user_id(user_id)


# Actualizar perfil de alumno
@router.put("/{user_id}", response_model=StudentResponse)
def update_student(
    user_id: int,
    student_update: StudentUpdate,
    service: StudentService = Depends(get_student_service)
):
    return service.update_student(user_id, student_update)