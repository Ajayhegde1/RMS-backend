# app/models/Restaurant.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    logo_svg = Column(String(255), nullable=True)
    cover_photo_svg = Column(String(255), nullable=True)
    branches = Column(String(255), nullable=True)  # Storing branches as a comma-separated string
    primary_number = Column(String(255), nullable=True)
    secondary_number = Column(String(255), nullable=True)
    active = Column(Boolean, default=True)
    restaurant_user_id = Column(Integer, ForeignKey('restaurant_user.id'))

    # Relationships
    restaurant_user = relationship('RestaurantUser', back_populates='restaurant')
    coupon = relationship('Coupon', back_populates='restaurant')
    raw_materials = relationship('RawMaterial', back_populates='restaurant')
    foods = relationship('Food', back_populates='restaurant')
    reviews = relationship('Review', back_populates='restaurant') 