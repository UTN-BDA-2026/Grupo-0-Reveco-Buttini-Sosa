from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.role import RoleRepository
from app.services.role import RoleService
from app.schemas.role import RoleCreate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(RoleRepository(db))


# Crear rol
@router.post("/", response_model=RoleResponse, status_code=201)
def create_role(
    role_data: RoleCreate,
    service: RoleService = Depends(get_role_service)
):
    return service.create_role(role_data)


# Obtener todos los roles
@router.get("/", response_model=list[RoleResponse])
def get_all_roles(
    service: RoleService = Depends(get_role_service)
):
    return service.get_all()


# Obtener rol por ID
@router.get("/{role_id}", response_model=RoleResponse)
def get_role_by_id(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    return service.get_by_id(role_id)