from sqlalchemy import Column, Numeric, String, Integer, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from models import Base
from models.UserRole import UserRole
from models.RolePermission import RolePermission

class DbBackup(Base):
    __tablename__ = "db_backup"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    file = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    isact = Column(Boolean, default=True, nullable=True)
