# app/models/FoodRawMaterial.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class FoodRawMaterial(Base):
    __tablename__ = 'food_raw_material'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    food_id = Column(Integer, ForeignKey('food.id'), nullable=False)
    raw_material_id = Column(Integer, ForeignKey('raw_material.id'), nullable=False)
    quantity = Column(Float, nullable=False)

    # Relationships
    food = relationship('Food', back_populates='food_raw_materials')
    raw_material = relationship('RawMaterial', back_populates='food_raw_materials')
