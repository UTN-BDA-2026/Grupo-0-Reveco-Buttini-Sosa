from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    legajo = Column(String(20), unique=True, nullable=False, index=True)
    carrera = Column(String(100), nullable=False)
    anio_ingreso = Column(Integer, nullable=False)

    # Relación con User
    user = relationship("User", back_populates="student")

    def __repr__(self):
        return f"<Student id={self.id} legajo={self.legajo}>"