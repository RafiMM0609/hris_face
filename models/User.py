from sqlalchemy import Column, String, ForeignKey, Integer, UUID, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from models import Base

class User(Base):
    __tablename__ = "user"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    nik = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    face_id = Column(String, nullable=False)
    client_id = Column(Integer, nullable=False, index=True)
    outlet_id = Column(Integer, nullable=False, index=True)
    password = Column(String, nullable=False)
    first_login = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP)
    isact = Column(Boolean, default=True)
    status = Column(Boolean, default=True)
    id_seq = Column(Integer, nullable
                    =True)
    id_user = Column(String(10), nullable=True)


