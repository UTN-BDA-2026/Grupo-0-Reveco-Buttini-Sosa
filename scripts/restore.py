import os
import json
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
        backup_data = json.load(f)

    with engine.connect() as conn:
        # Se elimina en orden inverso para respetar las FK
        conn.execute(text("DELETE FROM staff"))
        conn.execute(text("DELETE FROM teachers"))
        conn.execute(text("DELETE FROM students"))
        conn.execute(text("DELETE FROM users"))
        conn.execute(text("DELETE FROM roles"))

        # Se restaura en orden para respetar las FK
        for role in backup_data.get("roles", []):
            conn.execute(text("""
                INSERT INTO roles (id, name, description, created_at)
                VALUES (:id, :name, :description, :created_at)
            """), role)

        for user_data in backup_data.get("users", []):
            conn.execute(text("""
                INSERT INTO users (id, name, surname, username, email, password, role_id, created_at)
                VALUES (:id, :name, :surname, :username, :email, :password, :role_id, :created_at)
            """), user_data)

        for student in backup_data.get("students", []):
            conn.execute(text("""
                INSERT INTO students (id, user_id, legajo, carrera, anio_ingreso)
                VALUES (:id, :user_id, :legajo, :carrera, :anio_ingreso)
            """), student)

        for teacher in backup_data.get("teachers", []):
            conn.execute(text("""
                INSERT INTO teachers (id, user_id, legajo, departamento, titulo)
                VALUES (:id, :user_id, :legajo, :departamento, :titulo)
            """), teacher)

        for staff in backup_data.get("staff", []):
            conn.execute(text("""
                INSERT INTO staff (id, user_id, legajo, sector, cargo)
                VALUES (:id, :user_id, :legajo, :sector, :cargo)
            """), staff)

        conn.commit()

    print(f"✅ PostgreSQL restaurado correctamente")
    print(f"   roles: {len(backup_data['roles'])} | usuarios: {len(backup_data['users'])} | alumnos: {len(backup_data['students'])} | docentes: {len(backup_data['teachers'])} | administrativos: {len(backup_data['staff'])}")


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

    restore_postgres(f"{BACKUP_DIR}/{backups[-1]}")
    print("=== Restore completado ===")