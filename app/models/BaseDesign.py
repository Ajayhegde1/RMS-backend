#app/models/BaseDesign.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class BaseDesign(Base):
    __tablename__ = 'base_design'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    base_design_front_svg = Column(String(255))
    base_design_back_svg = Column(String(255))
    base_design_svg = Column(String(255))
    price = Column(Integer)
    active = Column(Boolean, default=True)
    vendor_id = Column(Integer, ForeignKey('vendor.id'))

    # Relationships
    vendor = relationship('Vendor', back_populates='base_design')
    cuisine = relationship('Cuisine', back_populates='base_design')
    nfc_design = relationship('NFCDesign', back_populates='base_design')

