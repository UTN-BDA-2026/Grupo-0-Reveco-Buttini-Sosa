from fastapi import FastAPI

from app.database.database import Base, engine


from app.models.user import User
from app.routes.user import router as user_router



#Crea las tablas en PostgreSQL si no existen
Base.metadata.create_all(bind=engine)


#Instancia principal de FastAPI
app = FastAPI(
        title="NEXO",
        description="API de Autenticacion y Sesiones de Usuario",
)

#Se registran las rutas que importe arriba, en modulos separados
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Welcome to LogCore"}