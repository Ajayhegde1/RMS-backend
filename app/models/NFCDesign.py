# app/models/NFCDesign.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class NFCDesign(Base):
    __tablename__ = 'nfc_design'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    design_name = Column(String(255))
    template_svg = Column(String(255))
    total_price = Column(Integer)
    active = Column(Boolean, default=True)
    generate_qr_id = Column(Integer, ForeignKey('generate_qr.id'))
    base_design_id = Column(Integer, ForeignKey('base_design.id'))
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'))

    # Relationships
    generate_qr = relationship('GenerateQR', back_populates='nfc_designs')
    cart = relationship('Cart', back_populates='nfc_design')
    base_design = relationship('BaseDesign', back_populates='nfc_design')
    cuisine = relationship('Cuisine', back_populates='nfc_design')
