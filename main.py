from fastapi import FastAPI

from app.database.database import Base
from app.database.database import engine

from app.models.log_model import Log

from app.routes.log_routes import router as log_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(log_router)


@app.get("/")
async def root():
    return {"message": "Welcome to LogCore"}