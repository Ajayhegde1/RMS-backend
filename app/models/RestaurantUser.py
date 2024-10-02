# app/models/RestaurantUser.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class RestaurantUser(Base):
    __tablename__ = 'restaurant_user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    phone_number = Column(String(255))
    active = Column(Boolean, default=True)

    # Relationships
    restaurant = relationship('Restaurant', back_populates='restaurant_user')
    customization_request = relationship('CustomizationRequest', back_populates='restaurant_user')
    generate_qr = relationship('GenerateQR', back_populates='restaurant_user')
    cart = relationship('Cart', back_populates='restaurant_user')
