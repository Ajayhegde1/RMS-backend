from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..services.RawMaterialService import RawMaterialService
from ..database import get_db
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
@router.post("/addRawMaterial")
async def create_raw_material(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received create raw material request: {data}")

    name = data.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")

    quantity = data.get("quantity", 0)
    price = data.get("price", 0)
    category_name = data.get("category")
    if not category_name:
        raise HTTPException(status_code=400, detail="Category is required")
    unit = data.get("unit")
    restaurant_id = data.get("restaurant_id")

    try:
        # Create or get the category first
        category = RawMaterialService.create_or_get_category(db=db, name=category_name)
        category_id = category.id

        # Check if a raw material with the same name and restaurant_id already exists
        existing_raw_material = RawMaterialService.get_raw_material_by_name(
            db=db, name=name, restaurant_id=restaurant_id
        )
        
        if existing_raw_material:
            # If a raw material with the same name and restaurant_id exists, return a conflict response
            raise HTTPException(status_code=409, detail="Raw material with the same name already exists for this restaurant")

        # Create the raw material with the category ID
        created_raw_material = RawMaterialService.create_raw_material(
            db=db, name=name, quantity=quantity, price=price, category_id=category_id, unit=unit, restaurant_id=restaurant_id
        )
        logger.info(f"Raw material created successfully with name: {name}")
        return {
            "statusCode": 200,
            "detail": "Raw material created successfully",
            "response": created_raw_material
        }
    except Exception as e:
        logger.error(f"Error creating raw material: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the raw material")

@router.get("/getAllRawMaterials")
async def get_all_raw_materials(db: Session = Depends(get_db)):
    raw_materials = RawMaterialService.get_all_raw_materials(db=db)
    return {
        "statusCode": 200,
        "detail": "Raw materials retrieved successfully",
        "response": raw_materials
    }

@router.get("/getRawMaterialById/{raw_material_id}")
async def get_raw_material_by_id(raw_material_id: int, db: Session = Depends(get_db)):
    raw_material = RawMaterialService.get_raw_material_by_id(db=db, raw_material_id=raw_material_id)
    if not raw_material:
        raise HTTPException(status_code=404, detail="Raw material not found")
    return {
        "statusCode": 200,
        "detail": "Raw material retrieved successfully",
        "response": raw_material
    }

@router.get("/getRawMaterialByName/search/{name}")
async def get_raw_material_by_name(name: str, restaurant_id: int, db: Session = Depends(get_db)):
    raw_materials = RawMaterialService.get_raw_material_by_name(db=db, name=name, restaurant_id=restaurant_id)
    if not raw_materials:
        raise HTTPException(status_code=404, detail="Raw material not found")
    return {
        "statusCode": 200,
        "detail": "Raw materials retrieved successfully",
        "response": raw_materials
    }

@router.get("/getAllRawMaterialsByRestaurant/{restaurant_id}")
async def get_all_raw_materials_by_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    raw_materials = RawMaterialService.get_all_raw_materials_by_restaurant(db=db, restaurant_id=restaurant_id)
    response_data = [
        {
            "id": rm[0].id,  # Accessing RawMaterialModel instance attributes
            "name": rm[0].name,
            "quantity": rm[0].quantity,
            "price": rm[0].price,
            "category_name": rm[1],  # Accessing category name directly from the tuple
            "unit": rm[0].unit,
            "restaurant_id": rm[0].restaurant_id
        }
        for rm in raw_materials
    ]
    return {
        "statusCode": 200,
        "detail": "Raw materials retrieved successfully",
        "response": response_data
    }
