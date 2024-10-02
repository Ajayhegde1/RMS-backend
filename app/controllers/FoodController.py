#app/controllers/FoodController.py
from fastapi import APIRouter, Depends, HTTPException, Request,File, UploadFile
from sqlalchemy.orm import Session
from ..services.FoodService import FoodService
from ..database import get_db
import logging
import boto3
import os
import time
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from ..models.FoodRawMaterial import FoodRawMaterial as FoodRawMaterial
from ..models.RawMaterial import RawMaterial as RawMaterial
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3_client = boto3.client(
    's3',
    region_name=os.getenv("DO_SPACES_REGION"),
    endpoint_url=os.getenv("SPACES_ENDPOINT"),
    aws_access_key_id=os.getenv("SPACES_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SPACES_SECRET_KEY"),
)


@router.post("/addFoodItem")
async def create_food(
    request: Request, 
    image: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    data = await request.form()
    logger.info(f"Received create food request: {data}")
    logger.info(f"uhuhuhuhuhuhuhhuh{type(data.get('is_veg')) }")


    # Upload image to DigitalOcean Spaces
    try:
        image_url = await upload_image_to_spaces(image)
        logger.info(f"HIHIHIHIHIHIHIHIHIHI{image_url}")
    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image")

    # Create food item
    try:
        created_food = FoodService.create_food(
            db=db, 
            name=data.get("name"), 
            restaurant_id=data.get("restaurant_id"),
            category=data.get("category"), 
            is_veg= data.get("is_veg").lower() == "true", 
            cuisine=data.get("cuisine"), 
            description=data.get("description"), 
            rating=data.get("rating"), 
            nutritional_value=data.get("nutritional_value"), 
            price=data.get("price"), 
            image=image_url,  # Store the URL in the DB
            youtube_link=data.get("youtube_link")
        )
    except HTTPException as e:
        logger.error(f"Error creating food: {e.detail}")
        raise e

    logger.info(f"Food created successfully with name: {data.get('name')}")

    return {
        "statusCode": 200,
        "detail": "Food created successfully",
        "response": created_food
    }
async def upload_image_to_spaces(image: UploadFile):
    try: 
        logger.info(f"jujuju{image.file}")
        # Generate a unique name for the image
        image_name = f"{os.path.splitext(image.filename)[0]}-{int(time.time())}{os.path.splitext(image.filename)[1]}"
        logger.info(f"hihihihi{image_name}")
        # Upload the image to DigitalOcean Spaces
        image.file.seek(0)
        s3_client.upload_fileobj(
            image.file,
            os.getenv("BUCKET_NAME"),
            image_name,
            ExtraArgs={"ACL": "public-read"}
        )

        # Construct the image URL
        image_url = f"{os.getenv('SPACES_ENDPOINT')}/{os.getenv('BUCKET_NAME')}/{image_name}"
        return image_url

    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        raise Exception("Failed to upload image")
@router.post("/addRawMaterialForFood")
async def add_raw_material_to_food(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received add raw material to food request: {data}")

    food_id = data.get("food_id")
    raw_material_id = data.get("raw_material_id")
    quantity = data.get("quantity")

    if not (food_id and raw_material_id and quantity):
        raise HTTPException(status_code=400, detail="food_id, raw_material_id, and quantity are required")

    created_food_raw_material = FoodService.add_raw_material_to_food(
        db=db, 
        food_id=food_id, 
        raw_material_id=raw_material_id, 
        quantity=quantity
    )
    logger.info(f"Raw material added to food successfully with food_id: {food_id} and raw_material_id: {raw_material_id}")

    return {
        "statusCode": 200,
        "detail": "Raw material added to food successfully",
        "response": created_food_raw_material
    }

@router.post("/addRawMaterialsObjForFood")
async def add_raw_materials_obj_to_food(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received add raw materials to food request: {data}")

    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="A list of raw material data is required")

    responses = []

    for item in data:
        food_id = item.get("food_id")
        raw_material_id = item.get("raw_material_id")
        quantity = item.get("quantity")

        if not (food_id and raw_material_id and quantity):
            logger.warning(f"Invalid data: {item}")
            continue

        try:
            quantity = float(quantity)  # Explicitly convert quantity to float
        except ValueError:
            logger.warning(f"Invalid quantity format: {quantity} for item: {item}")
            continue

        # Check if the food_id and raw_material_id combination already exists
        existing_record = db.query(FoodRawMaterial).filter_by(food_id=food_id, raw_material_id=raw_material_id).first()

        if existing_record:
            # If exists, update the quantity
            existing_record.quantity += quantity
            db.commit()
            db.refresh(existing_record)
            logger.info(f"Updated quantity of raw material in food with food_id: {food_id} and raw_material_id: {raw_material_id}")
            responses.append(existing_record)
        else:
            # If not exists, create a new record
            created_food_raw_material = FoodService.add_raw_material_to_food(
                db=db, 
                food_id=food_id, 
                raw_material_id=raw_material_id, 
                quantity=quantity
            )
            responses.append(created_food_raw_material)
            logger.info(f"Raw material added to food successfully with food_id: {food_id} and raw_material_id: {raw_material_id}")

    if not responses:
        raise HTTPException(status_code=400, detail="No valid raw material data provided")

    return {
        "statusCode": 200,
        "detail": "Raw materials added to food successfully",
        "response": responses
    }


@router.get("/getRawMaterialsForFood/{food_id}")
async def get_raw_materials_for_food(food_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching raw materials for food_id: {food_id}")

    # Query the database to get the raw materials associated with the food_id
    food_raw_materials = db.query(FoodRawMaterial, RawMaterial).join(
        RawMaterial, FoodRawMaterial.raw_material_id == RawMaterial.id
    ).filter(FoodRawMaterial.food_id == food_id).all()

    if not food_raw_materials:
        raise HTTPException(status_code=404, detail="No raw materials found for the given food_id")

    response = []
    for food_raw_material, raw_material in food_raw_materials:
        quantity_from_mapping = food_raw_material.quantity
        price = raw_material.price
        cost = quantity_from_mapping * price

        response.append({
            "raw_material_name": raw_material.name,
            "quantity": raw_material.quantity,
            "price": price,
            "mapped_quantity": quantity_from_mapping,
            "cost": cost
        })

    logger.info(f"Raw materials fetched successfully for food_id: {food_id}")
    return {
        "statusCode": 200,
        "detail": "Raw materials fetched successfully",
        "response": response
    }

@router.get("/getFoodById/{food_id}")
async def get_food_by_id(food_id: int, db: Session = Depends(get_db)):
    food = FoodService.get_food_by_id(db=db, food_id=food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    return {
        "statusCode": 200,
        "detail": "Food retrieved successfully",
        "response": food
    }

@router.get("/getAllFoodItemsByRestaurant/{restaurant_id}")
async def get_all_food_items_by_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    foods = FoodService.get_all_food_by_restaurant(db=db, restaurant_id=restaurant_id)
    logger.info("foods {foods}")
    return {
        "statusCode": 200,
        "detail": "Food items retrieved successfully",
        "response": foods
    }

@router.put("/editFood/{food_id}")
async def edit_food(food_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received edit food request: {data}")

    updated_food = FoodService.update_food(
        db=db, 
        food_id=food_id, 
        name=data.get("name"),
        category=data.get("category"),
        is_veg=data.get("is_veg"),
        cuisine=data.get("cuisine"),
        description=data.get("description"),
        rating=data.get("rating"),
        nutritional_value=data.get("nutritional_value"),
        price=data.get("price"),
        image=data.get("image"),
        youtube_link=data.get("youtube_link")
    )
    
    if not updated_food:
        raise HTTPException(status_code=404, detail="Food not found")

    logger.info(f"Food updated successfully with id: {food_id}")
    return {
        "statusCode": 200,
        "detail": "Food updated successfully",
        "response": updated_food
    }

@router.delete("/deleteFood/{food_id}")
async def delete_food(food_id: int, db: Session = Depends(get_db)):
    deleted_food = FoodService.delete_food(db=db, food_id=food_id)
    if not deleted_food:
        raise HTTPException(status_code=404, detail="Food not found")

    logger.info(f"Food deleted successfully with id: {food_id}")
    return {
        "statusCode": 200,
        "detail": "Food deleted successfully",
        "response": deleted_food
    }

@router.put("/updateYouTubeLink/{food_id}")
async def update_youtube_link(food_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    youtube_link = data.get("youtube_link")

    if not youtube_link:
        raise HTTPException(status_code=400, detail="YouTube link is required")

    updated_food = FoodService.update_food(
        db=db, 
        food_id=food_id, 
        youtube_link=youtube_link
    )

    if not updated_food:
        raise HTTPException(status_code=404, detail="Food not found")

    logger.info(f"YouTube link updated successfully for food id: {food_id}")
    return {
        "statusCode": 200,
        "detail": "YouTube link updated successfully",
        "response": updated_food
    }
