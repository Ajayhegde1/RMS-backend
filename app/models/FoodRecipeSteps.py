# app/models/FoodRecipeSteps.py

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class FoodRecipeSteps(Base):
    __tablename__ = 'food_recipe_steps'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    food_id = Column(Integer, ForeignKey('food.id'), nullable=False)
    step_number = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    image_svg = Column(String(255), nullable=True)

    # Relationships
    food = relationship('Food', back_populates='food_recipe_steps')
