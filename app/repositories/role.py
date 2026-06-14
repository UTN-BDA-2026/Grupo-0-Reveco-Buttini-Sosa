from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.role import RoleCreate


class RoleRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, role_data: RoleCreate) -> Role:
        try:
            role = Role(
                name=role_data.name,
                description=role_data.description
            )
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
            return role
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, role_id: int) -> Role | None:
        return self.db.query(Role).filter(Role.id == role_id).first()

    def get_by_name(self, name: str) -> Role | None:
        return self.db.query(Role).filter(Role.name == name).first()

    def get_all(self) -> list[Role]:
        return self.db.query(Role).all()