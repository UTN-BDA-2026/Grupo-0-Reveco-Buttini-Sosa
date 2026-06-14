from fastapi import HTTPException

from app.repositories.role import RoleRepository
from app.schemas.role import RoleCreate


class RoleService:

    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def create_role(self, role_data: RoleCreate):
        # Verifica que no exista un rol con el mismo nombre
        if self.role_repository.get_by_name(role_data.name):
            raise HTTPException(status_code=400, detail="Rol ya existente")
        return self.role_repository.create(role_data)

    def get_by_id(self, role_id: int):
        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return role

    def get_all(self):
        return self.role_repository.get_all()