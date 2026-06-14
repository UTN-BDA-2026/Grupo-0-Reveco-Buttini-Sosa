from fastapi import HTTPException

from app.repositories.staff import StaffRepository
from app.schemas.staff import StaffCreate, StaffUpdate


class StaffService:

    def __init__(self, staff_repository: StaffRepository):
        self.staff_repository = staff_repository

    def create_staff(self, user_id: int, staff_data: StaffCreate):
        # Verifica que el legajo no esté registrado
        if self.staff_repository.get_by_legajo(staff_data.legajo):
            raise HTTPException(status_code=400, detail="Legajo ya registrado")
        return self.staff_repository.create(user_id, staff_data)

    def get_by_user_id(self, user_id: int):
        staff = self.staff_repository.get_by_user_id(user_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Administrativo no encontrado")
        return staff

    def update_staff(self, user_id: int, staff_update: StaffUpdate):
        staff = self.staff_repository.update(user_id, staff_update)
        if not staff:
            raise HTTPException(status_code=404, detail="Administrativo no encontrado")
        return staff