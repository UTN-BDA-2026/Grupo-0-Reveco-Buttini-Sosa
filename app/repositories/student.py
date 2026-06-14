from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, student_data: StudentCreate) -> Student:
        try:
            student = Student(
                user_id=user_id,
                legajo=student_data.legajo,
                carrera=student_data.carrera,
                anio_ingreso=student_data.anio_ingreso
            )
            self.db.add(student)
            self.db.commit()
            self.db.refresh(student)
            return student
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_user_id(self, user_id: int) -> Student | None:
        return self.db.query(Student).filter(Student.user_id == user_id).first()

    def get_by_legajo(self, legajo: str) -> Student | None:
        return self.db.query(Student).filter(Student.legajo == legajo).first()

    def update(self, user_id: int, student_update: StudentUpdate) -> Student | None:
        try:
            student = self.get_by_user_id(user_id)
            if not student:
                return None
            if student_update.carrera: student.carrera = student_update.carrera
            if student_update.anio_ingreso: student.anio_ingreso = student_update.anio_ingreso
            self.db.commit()
            self.db.refresh(student)
            return student
        except Exception as e:
            self.db.rollback()
            raise e