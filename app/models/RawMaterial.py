from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class RawMaterial(Base):
    __tablename__ = 'raw_material'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True, unique=False, nullable=False)
    quantity = Column(Float, nullable=True)
    price = Column(Float, nullable=True)
    category_id = Column(Integer, ForeignKey('raw_material_category.id'), nullable=True)
    unit = Column(String(255), nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    # Relationships
    food_raw_materials = relationship('FoodRawMaterial', back_populates='raw_material')
    category = relationship('RawMaterialCategory', back_populates='raw_materials')
    restaurant = relationship('Restaurant', back_populates='raw_materials')
