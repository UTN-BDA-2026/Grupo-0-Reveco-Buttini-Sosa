
# Refactorizar persistencia en DB en el modulo Repositories
# En rputes solo tienen que estar los endpoints
from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.log_model import Log

from app.schemas.log_schema import LogCreate
from app.schemas.log_schema import LogResponse


router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/", response_model=LogResponse)
def create_log(
    log: LogCreate,
    db: Session = Depends(get_db)
):

    new_log = Log(

        service=log.service,

        level=log.level,

        event_type=log.event_type,

        message=log.message
    )


    db.add(new_log)

    db.commit()

    db.refresh(new_log)


    return new_log


