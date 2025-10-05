from sqlalchemy import(
    Column, 
    String, 
    Integer, 
    DateTime, 
    ForeignKey, 
    Boolean,
    Float,
    Numeric
)
from sqlalchemy.orm import relationship
from models import Base
from models.UserRole import UserRole
from models.RolePermission import RolePermission
from models.Attendance import Attendance
from models.TimeSheet import TimeSheet
from sqlalchemy.orm import foreign, remote
from sqlalchemy import and_
from models.User import User


class ClientOutlet(Base):
    __tablename__ = "client_outlet"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    client_id = Column(String, ForeignKey("client.id"), nullable=False,index=True)
    name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    region = Column(String, nullable=True)
    area = Column(String, nullable=True)
    address = Column(String, nullable=True)
    # longitude = Column(Float, nullable=True)
    # latitude = Column(Float, nullable=True)
    longitude = Column(Numeric(38, 25), nullable=True)
    latitude = Column(Numeric(38, 25), nullable=True)
    created_by = Column(String(36),nullable=True)
    updated_by = Column(String(36),nullable=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    isact = Column(Boolean, default=True)
    id_outlet = Column(String(10), nullable=True)
    distance_tolerance = Column(Float, nullable=True)
    wilayah = Column(ForeignKey("wilayah.id"), nullable=True, index=True)

    client = relationship("Client", back_populates="outlets")
    outlet_user = relationship(
        "User",
        back_populates="user_outlet",
        primaryjoin=and_(
            foreign(User.outlet_id) == id,
            User.isact == True
        )
    )
    attendance_outlet = relationship("Attendance", back_populates="outlets")
    timesheet_outlet = relationship("TimeSheet", back_populates="outlets")
    
    # Many-to-many relationship with User through UserOutlet
    user_outlets = relationship("UserOutlet", back_populates="outlet")
