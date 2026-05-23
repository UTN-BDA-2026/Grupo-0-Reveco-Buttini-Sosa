from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.hash import hash_password


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> User:
        user = User(
            name=user_create.name,
            surname=user_create.surname,
            username=user_create.username,
            email=user_create.email,
            password=hash_password(user_create.password),  # Se hashea antes de guardar
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None

        if user_update.name: user.name = user_update.name
        if user_update.surname: user.surname = user_update.surname
        if user_update.username: user.username = user_update.username
        if user_update.email: user.email = user_update.email
        if user_update.password:
            user.password = hash_password(user_update.password)  # Se hashea antes de actualizar

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user