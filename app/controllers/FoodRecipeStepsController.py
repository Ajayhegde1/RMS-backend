# app/controllers/FoodRecipeStepsController.py
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app.controllers.FoodController import upload_image_to_spaces
from ..services.FoodRecipeStepsService import FoodRecipeStepsService
from ..database import get_db
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/recipe_steps")
async def create_food_recipe_step(
    request: Request, 
    image: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    data = await request.form()
    logger.info(f"Received create food recipe step request: {data}")

    food_id = data.get("food_id")
    step_number = data.get("step_number")
    description = data.get("description")

    if not (food_id and step_number and description):
        raise HTTPException(status_code=400, detail="food_id, step_number, and description are required")

    # Upload image to DigitalOcean Spaces
    try:
        image_svg = await upload_image_to_spaces(image)
    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image")

    created_step = FoodRecipeStepsService.create_food_recipe_step(
        db=db, 
        food_id=food_id, 
        step_number=step_number, 
        description=description, 
        image_svg=image_svg  # Store the URL in the DB
    )
    logger.info(f"Recipe step created successfully with food_id: {food_id} and step_number: {step_number}")

    return {
        "statusCode": 200,
        "detail": "Recipe step created successfully",
        "response": created_step
    }

@router.put("/recipe_steps")
async def update_food_recipe_step(
    request: Request, 
    image: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    data = await request.form()
    logger.info(f"Received update food recipe step request: {data}")

    food_id = data.get("food_id")
    step_number = data.get("step_number")
    description = data.get("description")

    if not (food_id and step_number):
        raise HTTPException(status_code=400, detail="food_id and step_number are required")

    # Upload image to DigitalOcean Spaces if a new image is provided
    image_svg = None
    if image:
        try:
            image_svg = await upload_image_to_spaces(image)
        except Exception as e:
            logger.error(f"Failed to upload image: {e}")
            raise HTTPException(status_code=500, detail="Failed to upload image")

    updated_step = FoodRecipeStepsService.update_food_recipe_step(
        db=db, 
        food_id=food_id, 
        step_number=step_number, 
        description=description, 
        image_svg=image_svg
    )

    if not updated_step:
        raise HTTPException(status_code=404, detail="Recipe step not found")

    logger.info(f"Recipe step updated successfully with food_id: {food_id} and step_number: {step_number}")
    return {
        "statusCode": 200,
        "detail": "Recipe step updated successfully",
        "response": updated_step
    }

@router.delete("/recipe_steps")
async def delete_food_recipe_step(food_id: int, step_number: int, db: Session = Depends(get_db)):
    deleted_step = FoodRecipeStepsService.delete_food_recipe_step(db=db, food_id=food_id, step_number=step_number)
    if not deleted_step:
        raise HTTPException(status_code=404, detail="Recipe step not found")

    logger.info(f"Recipe step deleted successfully with food_id: {food_id} and step_number: {step_number}")
    return {
        "statusCode": 200,
        "detail": "Recipe step deleted successfully",
        "response": deleted_step
    }

@router.get("/recipe_steps/{food_id}")
async def get_food_recipe_steps(food_id: int, db: Session = Depends(get_db)):
    recipe_steps = FoodRecipeStepsService.get_food_recipe_steps(db=db, food_id=food_id)
    if not recipe_steps:
        raise HTTPException(status_code=404, detail="No recipe steps found for this food_id")

    steps_response = [{"step_number": step.step_number, "description": step.description, "image_svg": step.image_svg} for step in recipe_steps]

    logger.info(f"Recipe steps retrieved successfully for food_id: {food_id}")
    return {
        "statusCode": 200,
        "detail": "Recipe steps retrieved successfully",
        "response": steps_response
    }
