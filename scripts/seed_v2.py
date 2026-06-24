# Ejecutar con: python scripts/seed_v2.py
# Este script NO toca los datos existentes — solo agrega usuarios nuevos
# distribuidos a propósito entre los años 2018-2025 para que cada partición
# de la tabla students tenga datos y se puedan comparar tiempos de consulta.

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from app.database.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.staff import Staff
from app.utils.hash import hash_password
from sqlalchemy import text

fake = Faker("es")

DEFAULT_PASSWORD = "Contraseña123"

CARRERAS = ["Ingeniería en Sistemas", "Ingeniería Civil", "Ingeniería Electrónica", "Ingeniería Mecánica"]

# Cuántos alumnos nuevos crear por cada año — 625 x 8 años = 5000 alumnos nuevos
ALUMNOS_POR_ANIO = {
    2018: 625,
    2019: 625,
    2020: 625,
    2021: 625,
    2022: 625,
    2023: 625,
    2024: 625,
    2025: 625,
}


def fix_students_sequence(db):
    # La migración de particionado copió los datos viejos con sus IDs originales,
    # pero no actualizó la secuencia interna del SERIAL. Esto la sincroniza
    # con el máximo id real para evitar colisiones de llave duplicada.
    db.execute(text("""
        SELECT setval(
            pg_get_serial_sequence('students', 'id'),
            COALESCE((SELECT MAX(id) FROM students), 0) + 1,
            false
        )
    """))
    db.commit()
    print("  🔧 Secuencia de students sincronizada.")


def generar_username_unico(db, numero, intentos_max=20):
    for intento in range(intentos_max):
        base = fake.user_name()  # No-unique: evita agotar el pool interno de Faker
        sufijo = numero if intento == 0 else f"{numero}{intento}"
        username = f"{base}{sufijo}"
        existe = db.query(User).filter(User.username == username).first()
        if not existe:
            return username
    raise Exception("No se pudo generar un username único tras varios intentos")


def generar_email_unico(db, numero, intentos_max=20):
    for intento in range(intentos_max):
        sufijo = numero if intento == 0 else f"{numero}_{intento}"
        email = f"alumno.{sufijo}@gmail.com"
        existe = db.query(User).filter(User.email == email).first()
        if not existe:
            return email
    raise Exception("No se pudo generar un email único tras varios intentos")


def get_role_alumno(db):
    role = db.query(Role).filter(Role.name == "alumno").first()
    if not role:
        raise Exception("No existe el rol 'alumno'. Corré primero scripts/seed.py")
    return role.id


def get_next_legajo_number(db):
    # Busca el último legajo de alumno (prefijo "A") para no repetir números
    last = db.query(Student).filter(Student.legajo.like("A%")).order_by(Student.id.desc()).first()
    if not last:
        return 1
    return int(last.legajo[1:]) + 1


def seed_students_by_year(db):
    role_id = get_role_alumno(db)
    next_number = get_next_legajo_number(db)
    hashed = hash_password(DEFAULT_PASSWORD)

    total_creados = 0

    for anio, cantidad in ALUMNOS_POR_ANIO.items():
        print(f"  Creando {cantidad} alumnos para anio_ingreso={anio}...")

        for _ in range(cantidad):
            username = generar_username_unico(db, next_number)
            email = generar_email_unico(db, next_number)

            user = User(
                name=fake.first_name(),
                surname=fake.last_name(),
                username=username,
                email=email,
                password=hashed,
                role_id=role_id,
            )
            db.add(user)
            db.flush()  # Para obtener user.id antes del commit

            db.add(Student(
                user_id=user.id,
                legajo=f"A{str(next_number).zfill(5)}",
                carrera=fake.random_element(CARRERAS),
                anio_ingreso=anio
            ))

            next_number += 1
            total_creados += 1

    db.commit()
    print(f"  ✅ {total_creados} alumnos nuevos creados, distribuidos entre 2018 y 2025.")
    print(f"  🔑 Contraseña de todos los usuarios nuevos: {DEFAULT_PASSWORD}")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("=== Seeder v2 NEXO — distribución por año de ingreso ===")
        fix_students_sequence(db)
        seed_students_by_year(db)
        print("=== Seeder v2 completado ===")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()