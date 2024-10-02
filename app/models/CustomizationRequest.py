# app/models/CustomizationRequest.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class CustomizationRequest(Base):
    __tablename__ = 'customization_request'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    details = Column(String(255))
    active = Column(Boolean, default=True)
    restaurant_user_id = Column(Integer, ForeignKey('restaurant_user.id'))

    # Relationships
    restaurant_user = relationship('RestaurantUser', back_populates='customization_request')
