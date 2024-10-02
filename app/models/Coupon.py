# app/models/Coupon.py
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Coupon(Base):
    __tablename__ = 'coupon'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(255))
    discount = Column(Integer)
    discount_type = Column(Enum('percentage', 'rupeesOff', name='discount_type'))
    description = Column(String(255))
    expiry_date = Column(Date)
    active = Column(Boolean, default=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    # Relationships
    restaurant = relationship('Restaurant', back_populates='coupon')
