from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.user import UserRepository
from app.repositories.session import SessionRepository
from app.services.auth import AuthService
from app.schemas.user import UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)        # Repository de usuarios en Postgres
    session_repository = SessionRepository()    # Repository de sesiones en MongoDB
    return AuthService(user_repository, session_repository)


# Endpoint de login — recibe email y contraseña, devuelve token JWT
@router.post("/login")
def login(
    user_login: UserLogin,
    service: AuthService = Depends(get_auth_service)
):
    return service.login(user_login)


# Endpoint de validación — verifica si un token sigue activo
@router.get("/validate")
def validate_token(
    token: str,
    service: AuthService = Depends(get_auth_service)
):
    return service.validate_token(token)


# Endpoint de logout — invalida la sesión en MongoDB
@router.post("/logout")
def logout(
    token: str,
    service: AuthService = Depends(get_auth_service)
):
    return service.logout(token)