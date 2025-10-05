from sqlalchemy import Column, Integer, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class ClientWilayah(Base):
    __tablename__ = "client_wilayah"

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    id_wilayah = Column(Integer, ForeignKey("wilayah.id"), nullable=False)
    id_client = Column(Integer, nullable=False)
    isact = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), nullable=True, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime(timezone=True), nullable=True)
