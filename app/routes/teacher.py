from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.teacher import TeacherRepository
from app.services.teacher import TeacherService
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse

router = APIRouter(prefix="/teachers", tags=["Teachers"])


def get_teacher_service(db: Session = Depends(get_db)) -> TeacherService:
    return TeacherService(TeacherRepository(db))


# Crear perfil de docente
@router.post("/{user_id}", response_model=TeacherResponse, status_code=201)
def create_teacher(
    user_id: int,
    teacher_data: TeacherCreate,
    service: TeacherService = Depends(get_teacher_service)
):
    return service.create_teacher(user_id, teacher_data)


# Obtener perfil de docente por user_id
@router.get("/{user_id}", response_model=TeacherResponse)
def get_teacher(
    user_id: int,
    service: TeacherService = Depends(get_teacher_service)
):
    return service.get_by_user_id(user_id)


# Actualizar perfil de docente
@router.put("/{user_id}", response_model=TeacherResponse)
def update_teacher(
    user_id: int,
    teacher_update: TeacherUpdate,
    service: TeacherService = Depends(get_teacher_service)
):
    return service.update_teacher(user_id, teacher_update)