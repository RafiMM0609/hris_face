from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TempDataKaryawan(Base):
    __tablename__ = 'temp_data_karyawan'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nik = Column(String(50), nullable=False)
    employe_name = Column(String(255))
    name = Column(String(255))
    value = Column(Float)
