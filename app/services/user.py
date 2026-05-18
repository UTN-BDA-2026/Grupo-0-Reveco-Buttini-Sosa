from fastapi import HTTPException

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_create: UserCreate):
        # Verifica que el email no esté registrado
        if self.user_repository.get_by_email(user_create.email):
            raise HTTPException(status_code=400, detail="Email ya registrado")

        # Verifica que el username no esté registrado
        if self.user_repository.get_by_username(user_create.username):
            raise HTTPException(status_code=400, detail="Username ya registrado")

        return self.user_repository.create_user(user_create)

    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user

    def update_user(self, user_id: int, user_update: UserUpdate):
        # Verifica que el usuario exista
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verifica que el nuevo email no esté registrado por otro usuario
        if user_update.email:
            existing = self.user_repository.get_by_email(user_update.email)
            if existing and existing.id != user_id:
                raise HTTPException(status_code=400, detail="Email ya registrado")

        # Verifica que el nuevo username no esté registrado por otro usuario
        if user_update.username:
            existing = self.user_repository.get_by_username(user_update.username)
            if existing and existing.id != user_id:
                raise HTTPException(status_code=400, detail="Username ya registrado")

        return self.user_repository.update_user(user_id, user_update)

    def delete_user(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        self.user_repository.delete_user(user_id)
        return {"message": "Usuario eliminado correctamente"}