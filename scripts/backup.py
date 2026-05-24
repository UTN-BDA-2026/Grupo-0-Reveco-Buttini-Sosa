import os
import json
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# Directorio donde se guardan los backups
BACKUP_DIR = "backups"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def backup_postgres():
    print("Haciendo backup de PostgreSQL...")

    os.makedirs(BACKUP_DIR, exist_ok=True)

    backup_file = f"{BACKUP_DIR}/postgres_{TIMESTAMP}.json"

    # Se conecta a Postgres con SQLAlchemy
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    with engine.connect() as conn:
        # Exporta todos los usuarios
        result = conn.execute(text("SELECT * FROM users"))
        rows = result.mappings().all()
        users = [dict(row) for row in rows]

        # Convierte datetime a string para poder serializar a JSON
        for user_data in users:
            for key, value in user_data.items():
                if hasattr(value, 'isoformat'):
                    user_data[key] = value.isoformat()

    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    print(f"✅ Backup guardado en: {backup_file} ({len(users)} usuarios)")


if __name__ == "__main__":
    print(f"=== Backup NEXO - {TIMESTAMP} ===")
    backup_postgres()
    print("=== Backup completado ===")