from fastapi import HTTPException

from app.repositories.student import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:

    def __init__(self, student_repository: StudentRepository):
        self.student_repository = student_repository

    def create_student(self, user_id: int, student_data: StudentCreate):
        # Verifica que el legajo no esté registrado
        if self.student_repository.get_by_legajo(student_data.legajo):
            raise HTTPException(status_code=400, detail="Legajo ya registrado")
        return self.student_repository.create(user_id, student_data)

    def get_by_user_id(self, user_id: int):
        student = self.student_repository.get_by_user_id(user_id)
        if not student:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return student

    def update_student(self, user_id: int, student_update: StudentUpdate):
        student = self.student_repository.update(user_id, student_update)
        if not student:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return student