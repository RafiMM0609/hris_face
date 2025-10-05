from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, func
from models import Base

class RefreshReport(Base):
    __tablename__ = "refresh_report"

    id = Column(Integer, primary_key=True, autoincrement=True)
    billing_id = Column(String(36), nullable=False)
    last_refresh = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    isact = Column(Boolean, default=True)