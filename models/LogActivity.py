from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    DateTime, 
    Boolean, 
    JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base


class LogActivity(Base):
    __tablename__ = "log_activity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(String(36), nullable=False, index=True)
    username = Column(String(255), nullable=True)
    role = Column(Integer, nullable=True)
    action = Column(String(255), nullable=True)
    data_before = Column(JSON, nullable=True)
    data_after = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    target = Column(String(255), nullable=True)
    module = Column(String(255), nullable=True)
    isact = Column(Boolean, default=True)
    status_request = Column(String(100), nullable=True)
