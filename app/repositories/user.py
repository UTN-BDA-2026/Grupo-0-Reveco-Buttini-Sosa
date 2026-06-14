from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.hash import hash_password


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> User:
        try:
            # BEGIN TRANSACTION (ocurre junto o restaura todo)
            user = User(
                name=user_create.name,
                surname=user_create.surname,
                username=user_create.username,
                email=user_create.email,
                password=hash_password(user_create.password),
                role_id=user_create.role_id,  # Se agrega el role_id
            )
            self.db.add(user)
            self.db.commit()        # COMMIT — confirma la transacción
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()      # ROLLBACK — revierte todo si algo falla
            raise e

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        try:
            # BEGIN TRANSACTION
            user = self.get_by_id(user_id)
            if not user:
                return None

            if user_update.name: user.name = user_update.name
            if user_update.surname: user.surname = user_update.surname
            if user_update.username: user.username = user_update.username
            if user_update.email: user.email = user_update.email
            if user_update.password:
                user.password = hash_password(user_update.password)

            self.db.commit()        # COMMIT
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()      # ROLLBACK
            raise e

    def delete_user(self, user_id: int) -> User | None:
        try:
            # BEGIN TRANSACTION
            user = self.get_by_id(user_id)
            if not user:
                return None
            self.db.delete(user)
            self.db.commit()        # COMMIT
            return user
        except Exception as e:
            self.db.rollback()      # ROLLBACK
            raise e