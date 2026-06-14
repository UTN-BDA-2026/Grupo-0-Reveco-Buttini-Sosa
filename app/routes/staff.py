from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.staff import StaffRepository
from app.services.staff import StaffService
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse

router = APIRouter(prefix="/staff", tags=["Staff"])


def get_staff_service(db: Session = Depends(get_db)) -> StaffService:
    return StaffService(StaffRepository(db))


# Crear perfil de administrativo
@router.post("/{user_id}", response_model=StaffResponse, status_code=201)
def create_staff(
    user_id: int,
    staff_data: StaffCreate,
    service: StaffService = Depends(get_staff_service)
):
    return service.create_staff(user_id, staff_data)


# Obtener perfil de administrativo por user_id
@router.get("/{user_id}", response_model=StaffResponse)
def get_staff(
    user_id: int,
    service: StaffService = Depends(get_staff_service)
):
    return service.get_by_user_id(user_id)


# Actualizar perfil de administrativo
@router.put("/{user_id}", response_model=StaffResponse)
def update_staff(
    user_id: int,
    staff_update: StaffUpdate,
    service: StaffService = Depends(get_staff_service)
):
    return service.update_staff(user_id, staff_update)