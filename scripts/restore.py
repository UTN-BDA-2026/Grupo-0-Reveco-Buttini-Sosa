import os
import json
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

BACKUP_DIR = "backups"


def restore_postgres(backup_file: str):
    print(f"Restaurando PostgreSQL desde {backup_file}...")

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    with open(backup_file, "r", encoding="utf-8") as f:
        users = json.load(f)

    with engine.connect() as conn:
        # Se eliminan los usuarios existentes y se insertan los del backup
        conn.execute(text("DELETE FROM users"))

        for user_data in users:
            conn.execute(text("""
                INSERT INTO users (id, name, surname, username, email, password, created_at)
                VALUES (:id, :name, :surname, :username, :email, :password, :created_at)
            """), user_data)

        conn.commit()

    print(f"✅ PostgreSQL restaurado correctamente ({len(users)} usuarios)")


def list_backups():
    if not os.path.exists(BACKUP_DIR):
        print("No existe el directorio de backups")
        return None

    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("postgres_")])

    print("\n=== Backups disponibles ===")
    for i, f in enumerate(backups):
        print(f"  {i+1}. {f}")

    return backups


if __name__ == "__main__":
    backups = list_backups()

    if not backups:
        print("No hay backups disponibles")
        exit()

    # Usa el backup más reciente automáticamente
    restore_postgres(f"{BACKUP_DIR}/{backups[-1]}")

    print("=== Restore completado ===")