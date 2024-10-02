# app/models/Cart.py
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cart_price = Column(Integer)
    active = Column(Boolean, default=True)
    restaurant_user_id = Column(Integer, ForeignKey('restaurant_user.id'))
    nfc_design_id = Column(Integer, ForeignKey('nfc_design.id'))

    # Relationships
    restaurant_user = relationship('RestaurantUser', back_populates='cart')
    nfc_design = relationship('NFCDesign', back_populates='cart')
