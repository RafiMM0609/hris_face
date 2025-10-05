from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, func
from models import Base

class RefreshClientReport(Base):
    __tablename__ = "refresh_client_report"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, unique=True)
    last_refresh = Column(TIMESTAMP, nullable=True, server_default=func.now())
    isact = Column(Boolean, default=True)