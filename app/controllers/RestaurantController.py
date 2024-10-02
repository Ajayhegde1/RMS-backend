# app/controllers/RestaurantController.py
from fastapi import APIRouter, Depends, HTTPException, Request,File, UploadFile
from sqlalchemy.orm import Session
from ..models.Restaurant import Restaurant as RestaurantModel
from ..services.RestaurantService import RestaurantService
from ..services.RestaurantUserService import RestaurantUserService
from ..database import get_db
from ..middleware.jwt_middleware import JWTBearer
import logging
import boto3
import os
import time
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from ..schema import RestaurantCreateRequest 

router = APIRouter()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

s3_client = boto3.client(
    's3',
    region_name=os.getenv("DO_SPACES_REGION"),
    endpoint_url=os.getenv("SPACES_ENDPOINT"),
    aws_access_key_id=os.getenv("SPACES_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SPACES_SECRET_KEY"),
)


@router.post("/add_restaurant")
async def add_restaurant(
    # restaurant_data: RestaurantCreateRequest, 
     request: Request, 
     logo_image: UploadFile = File(...), 
      cover_image: UploadFile = File(...), 
    db: Session = Depends(get_db)
):  
    data = await request.form()
    logger.info(f"Received request to add restaurant with name: {data}")
    # logger.info(f"wwwwwwwww{logo_image}{cover_image}")
    try:
        image_url_logo = await upload_image_to_spaces(logo_image)
        image_url_cover = await upload_image_to_spaces(cover_image)
    except Exception as e:
        logger.error(f"Failed to upload image: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image")
    # Verify if the restaurant user exists
    restaurant_user = RestaurantUserService.get_user_by_id(db, data.get("restaurant_user_id"))
    if not restaurant_user:
        # logger.warning(f"Restaurant user ID {data.get("restaurant_user_id")} not found")
        raise HTTPException(status_code=404, detail="Restaurant user not found")

    # Convert branches list to a comma-separated string if provided
    branches_str = ",".join(data.get("branches")) if data.get("branches") else None

    # Create restaurant entry
    # restaurant = RestaurantModel(
    #     name=restaurant_data.name,
    #     logo_svg=restaurant_data.logo_svg,
    #     cover_photo_svg=restaurant_data.cover_photo_svg,
    #     restaurant_user_id=restaurant_data.restaurant_user_id,
    #     branches=branches_str,
    #     primary_number=restaurant_data.primary_number,
    #     secondary_number=restaurant_data.secondary_number
    # )
    restaurant = RestaurantModel(
        name=data.get("name"),
        logo_svg=image_url_logo,
        cover_photo_svg=image_url_cover,
        restaurant_user_id=data.get("restaurant_user_id"),
        branches=branches_str,
        primary_number=data.get("primary_number"),
        secondary_number=data.get("secondary_number")
    )
    db_restaurant = RestaurantService.create_restaurant(db=db, restaurant=restaurant)
    logger.info(f"Restaurant created successfully with ID: {db_restaurant.id}")

    return {"statusCode": 200, "detail": "Restaurant added successfully", "response": db_restaurant}


async def upload_image_to_spaces(image: UploadFile):
    try: 
        logger.info(f"jujuju{image.file}")
        # Generate a unique name for the image
        image_name = f"{os.path.splitext(image.filename)[0]}-{int(time.time())}{os.path.splitext(image.filename)[1]}"
        logger.info(f"hihihihi{image_name}")
        # Upload the image to DigitalOcean Spaces
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


@router.get("/restaurant/{restaurant_id}")
async def get_restaurant(restaurant_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    logger.info(f"Fetching restaurant details for ID: {restaurant_id}")
    
    restaurant = RestaurantService.get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        logger.warning(f"Restaurant ID {restaurant_id} not found")
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    logger.info(f"Restaurant details fetched for ID: {restaurant_id}")
    
    return {
        "statusCode": 200,
        "detail": "Restaurant details fetched successfully",
        "response": {
            "name": restaurant.name,
            "logo_svg": restaurant.logo_svg,
            "cover_photo_svg": restaurant.cover_photo_svg,
            "restaurant_user_id": restaurant.restaurant_user_id,
            "branches": restaurant.branches.split(",") if restaurant.branches else [],
            "primary_number": restaurant.primary_number,
            "secondary_number": restaurant.secondary_number
        }
    }

@router.get("/getRestaurantByUserId/{restaurantUser_id}")
async def get_restaurant(restaurantUser_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    logger.info(f"Fetching restaurant details for restaurant user ID: {restaurantUser_id}")
    
    restaurant = RestaurantService.get_restaurant_by_user_id(db, restaurantUser_id)
    if not restaurant:
        logger.warning(f"Restaurant User ID {restaurantUser_id} not found")
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    logger.info(f"Restaurant details fetched for restaurant user ID: {restaurantUser_id}")

    return {
        "statusCode": 200,
        "detail": "Restaurant details retrieved by restaurant user ID",
        "response": {
            "id": restaurant.id,
            "name": restaurant.name,
            "logo_svg": restaurant.logo_svg,
            "cover_photo_svg": restaurant.cover_photo_svg,
            "restaurant_user_id": restaurant.restaurant_user_id,
            "branches": restaurant.branches.split(",") if restaurant.branches else [],
            "primary_number": restaurant.primary_number,
            "secondary_number": restaurant.secondary_number
        }
    }

@router.put("/update_restaurant/{restaurant_id}")
async def update_restaurant(restaurant_id: int, request: Request, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    data = await request.json()
    logger.info(f"Received update request for restaurant ID: {restaurant_id} with data: {data}")
    
    updated_restaurant = RestaurantService.update_restaurant(db=db, restaurant_id=restaurant_id, update_data=data)
    if not updated_restaurant:
        logger.warning(f"Restaurant ID {restaurant_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    logger.info(f"Restaurant ID {restaurant_id} updated successfully")
    
    return {
        "statusCode": 200,
        "detail": "Restaurant updated successfully",
        "response": updated_restaurant
    }

@router.delete("/delete_restaurant/{restaurant_id}")
async def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    logger.info(f"Received delete request for restaurant ID: {restaurant_id}")
    
    deleted_restaurant = RestaurantService.delete_restaurant(db=db, restaurant_id=restaurant_id)
    if not deleted_restaurant:
        logger.warning(f"Restaurant ID {restaurant_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    logger.info(f"Restaurant ID {restaurant_id} marked as inactive")
    
    return {
        "statusCode": 200,
        "detail": "Restaurant deleted successfully (soft delete)",
        "response": deleted_restaurant
    }
