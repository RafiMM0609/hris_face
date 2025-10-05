from sqlalchemy import Column, Numeric, String, Integer, DateTime, ForeignKey, Boolean, and_
from sqlalchemy.orm import relationship
from models import Base
from models.UserRole import UserRole
from models.RolePermission import RolePermission  # Ensure this is correctly imported


class MasterPtkp(Base):
    __tablename__ = "m_ptkp"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    tipe = Column(String, nullable=True)
    amount = Column(Numeric(10, 6), nullable=True)
    kategori = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    isact = Column(Boolean, default=True)
    keterangan = Column(String, nullable=True)

    # Relasi ke User
    users_ptkp = relationship("User", back_populates="ptkp_rel", foreign_keys="User.ptkp")