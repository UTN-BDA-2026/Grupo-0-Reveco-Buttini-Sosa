import os
import jwt

from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

# Se leen las variables de entorno
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION"))

# Genera el token JWT con user_id, username y fecha de expiración
def create_token(user_id: int, username: str) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=JWT_EXPIRATION)  # Fecha de expiración
    }

    # Se genera y devuelve el token firmado con la clave secreta
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


# Verifica y decodifica el token JWT si expiro lanza error
def decode_token(token: str) -> dict:
    # Se decodifica el token y se devuelve el payload
    # Si el token es inválido o expiró lanza una excepción automáticamente
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])