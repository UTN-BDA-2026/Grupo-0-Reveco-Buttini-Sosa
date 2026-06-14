from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    legajo = Column(String(20), unique=True, nullable=False, index=True)
    sector = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)

    # Relación con User
    user = relationship("User", back_populates="staff")

    def __repr__(self):
        return f"<Staff id={self.id} legajo={self.legajo}>"