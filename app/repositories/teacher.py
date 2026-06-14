from sqlalchemy.orm import Session

from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate


class TeacherRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, teacher_data: TeacherCreate) -> Teacher:
        try:
            teacher = Teacher(
                user_id=user_id,
                legajo=teacher_data.legajo,
                departamento=teacher_data.departamento,
                titulo=teacher_data.titulo
            )
            self.db.add(teacher)
            self.db.commit()
            self.db.refresh(teacher)
            return teacher
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_user_id(self, user_id: int) -> Teacher | None:
        return self.db.query(Teacher).filter(Teacher.user_id == user_id).first()

    def get_by_legajo(self, legajo: str) -> Teacher | None:
        return self.db.query(Teacher).filter(Teacher.legajo == legajo).first()

    def update(self, user_id: int, teacher_update: TeacherUpdate) -> Teacher | None:
        try:
            teacher = self.get_by_user_id(user_id)
            if not teacher:
                return None
            if teacher_update.departamento: teacher.departamento = teacher_update.departamento
            if teacher_update.titulo: teacher.titulo = teacher_update.titulo
            self.db.commit()
            self.db.refresh(teacher)
            return teacher
        except Exception as e:
            self.db.rollback()
            raise e