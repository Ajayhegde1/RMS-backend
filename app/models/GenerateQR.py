# app/models/GenerateQR.py
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class GenerateQR(Base):
    __tablename__ = 'generate_qr'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    review_page_link = Column(String(255))
    qr_code_path = Column(String(255))
    platform_name = Column(String(255))
    orientation = Column(Enum('horizontal', 'vertical', name='qr_orientation'))
    review_text = Column(String(255))
    active = Column(Boolean, default=True)
    restaurant_user_id = Column(Integer, ForeignKey('restaurant_user.id'))
    platform_id = Column(Integer, ForeignKey('platform.id'))

    # Relationships
    restaurant_user = relationship('RestaurantUser', back_populates='generate_qr')
    nfc_designs = relationship('NFCDesign', back_populates='generate_qr')
    platform = relationship('Platform', back_populates='generate_qr')
