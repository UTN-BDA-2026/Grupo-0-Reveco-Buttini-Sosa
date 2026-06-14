from fastapi import FastAPI

from app.database.database import Base, engine

#Modelos - necesarios para que SQLAlchemy cree las tablas postgreSQL
from app.models.user import User
from app.models.role import Role
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.staff import Staff

#Rutas
from app.routes.user import router as user_router
from app.routes.role import router as role_router
from app.routes.student import router as student_router
from app.routes.teacher import router as teacher_router
from app.routes.staff import router as staff_router
from app.routes.auth import router as auth_router


#Crea las tablas en PostgreSQL si no existen
Base.metadata.create_all(bind=engine)


#Instancia principal de FastAPI
app = FastAPI(
        title="NEXO",
        description="API de Autenticacion y Sesiones de Usuario",
)

#Se registran las rutas que importe arriba, en modulos separados
app.include_router(user_router)
app.include_router(role_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(staff_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Welcome to LogCore"}