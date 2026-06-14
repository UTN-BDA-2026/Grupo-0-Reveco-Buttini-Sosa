from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    legajo = Column(String(20), unique=True, nullable=False, index=True)
    departamento = Column(String(100), nullable=False)
    titulo = Column(String(100), nullable=False)

    # Relación con User
    user = relationship("User", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher id={self.id} legajo={self.legajo}>"