# app/services/FoodRecipeStepsService.py

from sqlalchemy.orm import Session
from ..models.FoodRecipeSteps import FoodRecipeSteps as FoodRecipeStepsModel

class FoodRecipeStepsService:
    @staticmethod
    def create_food_recipe_step(db: Session, food_id: int, step_number: int, description: str, image_svg: str = None):
        food_recipe_step = FoodRecipeStepsModel(
            food_id=food_id,
            step_number=step_number,
            description=description,
            image_svg=image_svg
        )
        db.add(food_recipe_step)
        db.commit()
        db.refresh(food_recipe_step)
        return food_recipe_step

    @staticmethod
    def update_food_recipe_step(db: Session, food_id: int, step_number: int, description: str = None, image_svg: str = None):
        food_recipe_step = db.query(FoodRecipeStepsModel).filter(
            FoodRecipeStepsModel.food_id == food_id,
            FoodRecipeStepsModel.step_number == step_number
        ).first()

        if not food_recipe_step:
            return None

        if description:
            food_recipe_step.description = description
        if image_svg:
            food_recipe_step.image_svg = image_svg

        db.commit()
        db.refresh(food_recipe_step)
        return food_recipe_step

    @staticmethod
    def delete_food_recipe_step(db: Session, food_id: int, step_number: int):
        food_recipe_step = db.query(FoodRecipeStepsModel).filter(
            FoodRecipeStepsModel.food_id == food_id,
            FoodRecipeStepsModel.step_number == step_number
        ).first()

        if not food_recipe_step:
            return None

        db.delete(food_recipe_step)
        db.commit()
        return food_recipe_step

    @staticmethod
    def get_food_recipe_steps(db: Session, food_id: int):
        return db.query(FoodRecipeStepsModel).filter(FoodRecipeStepsModel.food_id == food_id).all()
