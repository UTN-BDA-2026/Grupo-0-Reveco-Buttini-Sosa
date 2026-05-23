from passlib.context import CryptContext

# Se configura el contexto de encriptación usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Recibe la contraseña en texto plano y devuelve el hash
    # Este hash es el que se guarda en la base de datos
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Compara la contraseña ingresada con el hash guardado
    # Devuelve True si coinciden, False si no
    return pwd_context.verify(plain_password, hashed_password)