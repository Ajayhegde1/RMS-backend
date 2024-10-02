# app/models/Vendor.py
from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Vendor(Base):
    __tablename__ = 'vendor'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    phone_number = Column(String(255))
    role = Column(Enum('admin', 'user', name='vendor_roles'))
    active = Column(Boolean, default=True)
    #shopify_access_token = Column(String, nullable=True) 

    # Relationships
    base_design = relationship('BaseDesign', back_populates='vendor')