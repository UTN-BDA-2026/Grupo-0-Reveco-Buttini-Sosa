from fastapi import HTTPException

from app.repositories.teacher import TeacherRepository
from app.schemas.teacher import TeacherCreate, TeacherUpdate


class TeacherService:

    def __init__(self, teacher_repository: TeacherRepository):
        self.teacher_repository = teacher_repository

    def create_teacher(self, user_id: int, teacher_data: TeacherCreate):
        # Verifica que el legajo no esté registrado
        if self.teacher_repository.get_by_legajo(teacher_data.legajo):
            raise HTTPException(status_code=400, detail="Legajo ya registrado")
        return self.teacher_repository.create(user_id, teacher_data)

    def get_by_user_id(self, user_id: int):
        teacher = self.teacher_repository.get_by_user_id(user_id)
        if not teacher:
            raise HTTPException(status_code=404, detail="Docente no encontrado")
        return teacher

    def update_teacher(self, user_id: int, teacher_update: TeacherUpdate):
        teacher = self.teacher_repository.update(user_id, teacher_update)
        if not teacher:
            raise HTTPException(status_code=404, detail="Docente no encontrado")
        return teacher