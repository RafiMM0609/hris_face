from sqlalchemy import Column, Numeric, String, Integer, DateTime, ForeignKey, Boolean, and_
from sqlalchemy.orm import relationship
from models import Base
from models.UserRole import UserRole
from models.RolePermission import RolePermission  # Ensure this is correctly imported


class PajakTer(Base):
    __tablename__ = "pajak_ter"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    salary = Column(Numeric(10, 6), nullable=True)
    percent = Column(Numeric(10, 6), nullable=True)
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    isact = Column(Boolean, default=True)