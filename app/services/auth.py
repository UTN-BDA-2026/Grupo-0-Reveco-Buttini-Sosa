from fastapi import HTTPException

from app.repositories.user import UserRepository
from app.repositories.session import SessionRepository
from app.schemas.user import UserLogin
from app.utils.hash import verify_password
from app.utils.jwt import create_token, decode_token


class AuthService:

    def __init__(self, user_repository: UserRepository, session_repository: SessionRepository):
        self.user_repository = user_repository
        self.session_repository = session_repository

    def login(self, user_login: UserLogin):
        # Busca el usuario por email en Postgres
        user = self.user_repository.get_by_email(user_login.email)

        # Si el usuario no existe guarda sesión fallida y devuelve error
        if not user:
            self.session_repository.create_session(
                user_id=None,
                username=user_login.email,
                token=None,
                success=False,
                reason="Usuario no encontrado"
            )
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        # Verifica la contraseña contra el hash guardado en Postgres
        if not verify_password(user_login.password, user.password):
            self.session_repository.create_session(
                user_id=user.id,
                username=user.username,
                token=None,
                success=False,
                reason="Contraseña incorrecta"
            )
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        # Si las credenciales son correctas genera el token JWT
        token = create_token(user.id, user.username)

        # Guarda la sesión exitosa en MongoDB
        self.session_repository.create_session(
            user_id=user.id,
            username=user.username,
            token=token,
            success=True
        )

        # Devuelve el token y los datos básicos del usuario
        return {
            "token": token,
            "user_id": user.id,
            "username": user.username
        }

    def validate_token(self, token: str):
        # Verifica que la sesión exista y esté activa en MongoDB
        session = self.session_repository.get_session_by_token(token)
        if not session:
            raise HTTPException(status_code=401, detail="Sesión inválida o expirada")

        # Decodifica el token y verifica que no haya expirado
        try:
            payload = decode_token(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        return {
            "valid": True,
            "user_id": payload["user_id"],
            "username": payload["username"]
        }

    def logout(self, token: str):
        # Invalida la sesión en MongoDB
        invalidated = self.session_repository.invalidate_session(token)
        if not invalidated:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")
        return {"message": "Sesión cerrada correctamente"}