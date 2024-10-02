#app/models/Cuisine.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Cuisine(Base):
    __tablename__ = 'cuisine'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    cuisine_image_svg = Column(String(255))
    active = Column(Boolean, default=True)
    base_design_id = Column(Integer, ForeignKey('base_design.id'))

    # Relationships
    base_design = relationship('BaseDesign', back_populates='cuisine')
    nfc_design = relationship('NFCDesign', back_populates='cuisine')