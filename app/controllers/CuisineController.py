# app/controllers/CuisineController.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models.Cuisine import Cuisine as CuisineModel
from ..services.CuisineService import CuisineService
from ..database import get_db

import logging

router = APIRouter()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/addCuisine")
async def add_cuisine(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received add cuisine request: {data}")

    name = data.get("name")
    cuisine_image_svg = data.get("cuisine_image_svg")
    base_design_id = data.get("base_design_id")

    if not (name and cuisine_image_svg and base_design_id):
        logger.warning("Missing required fields in add cuisine request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    cuisine = CuisineModel(
        name=name,
        cuisine_image_svg=cuisine_image_svg,
        base_design_id=base_design_id
    )

    created_cuisine = CuisineService.create_cuisine(db=db, cuisine_data=cuisine)
    logger.info(f"Cuisine {name} created successfully")

    return {"statusCode": 200, "detail": "Cuisine added successfully", "response": created_cuisine}

@router.get("/cuisines/{base_design_id}")
async def get_cuisines_by_base_design(base_design_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching cuisines for base_design_id: {base_design_id}")

    cuisines = CuisineService.get_cuisines_by_base_design_id(db, base_design_id)
    if not cuisines:
        logger.warning(f"No cuisines found for base_design_id: {base_design_id}")
        raise HTTPException(status_code=404, detail="No cuisines found")

    logger.info(f"Cuisines fetched for base_design_id: {base_design_id}")
    return {"statusCode": 200, "detail": "Cuisines fetched successfully", "response": cuisines}

@router.put("/updateCuisine/{cuisine_id}")
async def update_cuisine(cuisine_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received update cuisine request: {data}")

    updated_cuisine = CuisineService.update_cuisine(db=db, cuisine_id=cuisine_id, cuisine_data=data)
    if not updated_cuisine:
        logger.warning(f"Cuisine with ID {cuisine_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Cuisine not found")

    logger.info(f"Cuisine ID {cuisine_id} updated successfully")
    return {"statusCode": 200, "detail": "Cuisine updated successfully", "response": updated_cuisine}

@router.delete("/deleteCuisine/{cuisine_id}")
async def delete_cuisine(cuisine_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received delete cuisine request for cuisine_id: {cuisine_id}")

    deleted_cuisine = CuisineService.delete_cuisine(db=db, cuisine_id=cuisine_id)
    if not deleted_cuisine:
        logger.warning(f"Cuisine with ID {cuisine_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Cuisine not found")

    logger.info(f"Cuisine ID {cuisine_id} marked as inactive")
    return {"statusCode": 200, "detail": "Cuisine deleted successfully (soft delete)", "response": deleted_cuisine}

