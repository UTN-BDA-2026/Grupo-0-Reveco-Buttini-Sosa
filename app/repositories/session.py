from datetime import datetime, timezone, timedelta

from app.database.mongo import sessions_collection


class SessionRepository:

    def create_session(self, user_id: int, username: str, token: str, success: bool, reason: str = None) -> dict:
        # Se arma el documento base que se va a guardar en MongoDB
        session = {
            "user_id": user_id,
            "username": username,
            "status": "success" if success else "failed",
            "created_at": datetime.now(timezone.utc),
            "ip_address": None,  # Se puede completar más adelante
        }

        if success:
            # Si el login fue exitoso se agregan los campos del token y la expiración
            session["token"] = token
            session["expires_at"] = datetime.now(timezone.utc) + timedelta(seconds=3600)
            session["is_active"] = True
        else:
            # Si el login falló se agrega el motivo del fallo
            session["reason"] = reason
            session["is_active"] = False

        # Se inserta el documento en la colección sessions de MongoDB
        result = sessions_collection.insert_one(session)

        # Se agrega el id generado por MongoDB al documento y se devuelve
        session["_id"] = str(result.inserted_id)
        return session

    def get_session_by_token(self, token: str) -> dict | None:
        # Busca una sesión activa por token
        return sessions_collection.find_one({"token": token, "is_active": True})

    def invalidate_session(self, token: str) -> bool:
        # Marca la sesión como inactiva — usado en logout
        result = sessions_collection.update_one(
            {"token": token},
            {"$set": {"is_active": False}}
        )
        return result.modified_count > 0