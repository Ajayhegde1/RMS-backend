# app/models/Food.py
from sqlalchemy import Column, Integer, String, Boolean, Float,ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Food(Base):
    __tablename__ = 'food'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    category = Column(String(255), nullable=True)
    is_veg = Column(Boolean, nullable=True)
    cuisine = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    rating = Column(Float, nullable=True)
    nutritional_value = Column(String(255), nullable=True)
    price = Column(Float, default=0, nullable=True)
    image = Column(String(255), nullable=True)
    steps = Column(String(255), nullable=True)
    youtube_link = Column(String(255), nullable=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    # Relationships
    restaurant = relationship('Restaurant', back_populates='foods')
    food_raw_materials = relationship('FoodRawMaterial', back_populates='food')
    food_recipe_steps = relationship('FoodRecipeSteps', back_populates='food')
