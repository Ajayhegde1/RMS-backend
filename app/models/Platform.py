# app/models/Platform.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Platform(Base):
    __tablename__ = 'platform'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, index=True)
    active = Column(Boolean, default=True)

    # Relationships
    generate_qr = relationship('GenerateQR', back_populates='platform')
