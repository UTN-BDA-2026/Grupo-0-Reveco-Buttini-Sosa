# Ejecutar con: python scripts/seed.py
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

fake = Faker("es")

# Contraseña fija para todos los usuarios de prueba
DEFAULT_PASSWORD = "Contraseña123"

# Distribución de usuarios por rol
ROLES = [
    {"name": "alumno",         "description": "Estudiante de la institución"},
    {"name": "docente",        "description": "Profesor de la institución"},
    {"name": "administrativo", "description": "Personal administrativo"},
]

CARRERAS = ["Ingeniería en Sistemas", "Ingeniería Civil", "Ingeniería Electrónica", "Ingeniería Mecánica"]
DEPARTAMENTOS = ["Matemática", "Física", "Sistemas", "Electrónica", "Civil"]
TITULOS = ["Ingeniero", "Licenciado", "Magíster", "Doctor"]
SECTORES = ["Secretaría", "Bedelía", "Tesorería", "Rectorado"]
CARGOS = ["Jefe de área", "Auxiliar administrativo", "Coordinador", "Asistente"]


def seed_roles(db):
    # Verifica si ya existen roles
    existing = db.query(Role).count()
    if existing > 0:
        print(f"  Ya existen {existing} roles — omitiendo.")
        return {r.name: r.id for r in db.query(Role).all()}

    print("  Creando roles...")
    roles = {}
    for role_data in ROLES:
        role = Role(name=role_data["name"], description=role_data["description"])
        db.add(role)
        db.flush()  # Para obtener el id sin hacer commit todavía
        roles[role.name] = role.id

    db.commit()
    print(f"  ✅ {len(roles)} roles creados.")
    return roles


def seed_users(db, roles):
    # Verifica si ya hay usuarios cargados
    existing = db.query(User).count()
    if existing > 0:
        print(f"  Ya existen {existing} usuarios — omitiendo.")
        return

    print("  Creando 200 usuarios de prueba...")
    hashed = hash_password(DEFAULT_PASSWORD)  # Se hashea una sola vez para todos

    # Distribución: 140 alumnos, 40 docentes, 20 administrativos
    distribution = (
        [(roles["alumno"], "alumno")] * 140 +
        [(roles["docente"], "docente")] * 40 +
        [(roles["administrativo"], "administrativo")] * 20
    )

    for i, (role_id, role_name) in enumerate(distribution):
        user = User(
            name=fake.first_name(),
            surname=fake.last_name(),
            username=fake.unique.user_name(),
            email=f"{fake.unique.first_name().lower()}.{fake.unique.last_name().lower()}{i}@gmail.com",
            password=hashed,
            role_id=role_id,
        )
        db.add(user)
        db.flush()  # Para obtener el user.id antes del commit

        # Crea el perfil según el rol
        if role_name == "alumno":
            db.add(Student(
                user_id=user.id,
                legajo=f"A{str(i+1).zfill(5)}",
                carrera=fake.random_element(CARRERAS),
                anio_ingreso=fake.random_int(min=2018, max=2025)
            ))
        elif role_name == "docente":
            db.add(Teacher(
                user_id=user.id,
                legajo=f"D{str(i+1).zfill(5)}",
                departamento=fake.random_element(DEPARTAMENTOS),
                titulo=fake.random_element(TITULOS)
            ))
        elif role_name == "administrativo":
            db.add(Staff(
                user_id=user.id,
                legajo=f"S{str(i+1).zfill(5)}",
                sector=fake.random_element(SECTORES),
                cargo=fake.random_element(CARGOS)
            ))

    db.commit()
    print(f"  ✅ 200 usuarios creados (140 alumnos, 40 docentes, 20 administrativos).")
    print(f"  🔑 Contraseña de todos los usuarios: {DEFAULT_PASSWORD}")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("=== Seeder NEXO ===")
        roles = seed_roles(db)
        seed_users(db, roles)
        print("=== Seeder completado ===")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()