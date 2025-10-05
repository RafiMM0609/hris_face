from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    DateTime, 
    ForeignKey, 
    Boolean, 
    Numeric,
)
from sqlalchemy.orm import relationship
from models import Base


class MobileVersion(Base):
    __tablename__ = "mobile_version"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    version = Column(String, nullable=False, index=True)
    change_log = Column(String, nullable=True)
    link = Column(String, nullable=True)
    link_ios = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True))