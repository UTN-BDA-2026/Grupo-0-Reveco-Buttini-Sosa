#ejecutar con python scripts/seeder.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from app.database.database import SessionLocal
from app.models.user import User
from app.utils.hash import hash_password

fake = Faker("es") 

# Contraseña fija para todos los usuarios de prueba
DEFAULT_PASSWORD = "Contraseña123"

def seed_users():
    db = SessionLocal()

    try:
        # Verifica si ya hay usuarios cargados
        existing = db.query(User).count()
        if existing > 0:
            print(f"Ya existen {existing} usuarios en la base de datos.")
            return

        print("Creando 200 usuarios de prueba...")
        hashed = hash_password(DEFAULT_PASSWORD)  # Se hashea una sola vez para todos

        users = []
        for i in range(200):
            user = User(
                name=fake.first_name(),
                surname=fake.last_name(),
                username=fake.unique.user_name(),
                email = f"{fake.first_name().lower()}.{fake.last_name().lower()}@gmail.com",
                password=hashed,
            )
            users.append(user)

        # Se insertan todos los usuarios en una sola transacción
        db.add_all(users)
        db.commit()

        print(f"✅ 200 usuarios creados correctamente.")
        print(f" Contraseña de todos los usuarios: {DEFAULT_PASSWORD}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear usuarios: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()