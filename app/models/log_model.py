from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Text

from datetime import datetime

from app.database.database import Base


class Log(Base):

    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    service = Column(String, nullable=False)
    level = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    message = Column(Text, nullable=False)