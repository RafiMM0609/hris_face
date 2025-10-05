from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from models import Base
import uuid

class DefaultPassword(Base):
    __tablename__ = "defaultpassword"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    emp_id = Column(String(36), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
