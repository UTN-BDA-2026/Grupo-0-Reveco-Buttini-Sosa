from pydantic import BaseModel

from datetime import datetime


class LogCreate(BaseModel):     #valida entradas de logs

    service: str
    level: str
    event_type: str
    message: str


class LogResponse(LogCreate):   #estructura la respuesta o salida al cliente 

    id: int
    timestamp: datetime
    class Config:
        from_attributes = True