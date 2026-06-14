import os
import json
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

BACKUP_DIR = "backups"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def export_table(conn, table_name):
    result = conn.execute(text(f"SELECT * FROM {table_name}"))
    rows = result.mappings().all()
    data = [dict(row) for row in rows]

    # Convierte datetime a string para serializar a JSON
    for record in data:
        for key, value in record.items():
            if hasattr(value, 'isoformat'):
                record[key] = value.isoformat()

    return data


def backup_postgres():
    print("Haciendo backup de PostgreSQL...")

    os.makedirs(BACKUP_DIR, exist_ok=True)

    backup_file = f"{BACKUP_DIR}/postgres_{TIMESTAMP}.json"

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    with engine.connect() as conn:
        backup_data = {
            "roles":    export_table(conn, "roles"),
            "users":    export_table(conn, "users"),
            "students": export_table(conn, "students"),
            "teachers": export_table(conn, "teachers"),
            "staff":    export_table(conn, "staff"),
        }

    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Backup guardado en: {backup_file}")
    print(f"   roles: {len(backup_data['roles'])} | usuarios: {len(backup_data['users'])} | alumnos: {len(backup_data['students'])} | docentes: {len(backup_data['teachers'])} | administrativos: {len(backup_data['staff'])}")


if __name__ == "__main__":
    print(f"=== Backup NEXO - {TIMESTAMP} ===")
    backup_postgres()
    print("=== Backup completado ===")