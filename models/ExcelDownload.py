from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, CHAR
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from models import Base

class ExcelDownload(Base):
    __tablename__ = 'excel_download'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    file = Column(Text, nullable=False)
    modul_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(CHAR(36), nullable=False)
    updated_by = Column(CHAR(36), nullable=False)
    isact = Column(Boolean, default=True)