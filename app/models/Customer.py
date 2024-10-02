# app/models/Customer.py
from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    age = Column(Integer)
    dob = Column(Date)
    phone_number = Column(String(255))
    date_added = Column(Date, default=date.today)
    active = Column(Boolean, default=True)
    # shopify_access_token = Column(String, nullable=True)
