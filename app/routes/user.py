from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


# Crear usuario
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_create: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return service.create_user(user_create)


# Obtener usuario por ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.get_user_by_id(user_id)


# Actualizar usuario
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return service.update_user(user_id, user_update)


# Eliminar usuario
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return service.delete_user(user_id)