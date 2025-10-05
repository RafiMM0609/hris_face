from sqlalchemy import Column, Numeric, String, Integer, DateTime, ForeignKey, Boolean, and_
from sqlalchemy.orm import relationship
from models import Base


class Wilayah(Base):
    __tablename__ = "wilayah"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    isact = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)


    user_wilayahs = relationship("UserWilayah", back_populates="wilayah")

