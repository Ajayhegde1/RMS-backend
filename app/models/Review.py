from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    phone_number = Column(String(255), nullable=False)
    active = Column(Boolean, default=True)
    email_id = Column(String(255), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), nullable=False)

    # Relationships
    restaurant = relationship('Restaurant', back_populates='reviews')
