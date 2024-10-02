#app/controllers/RestaurantUserController
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models.RestaurantUser import RestaurantUser as RestaurantUserModel
from ..services.RestaurantUserService import RestaurantUserService
from ..database import get_db
from ..utils.jwt import create_access_token
from ..middleware.jwt_middleware import JWTBearer
from ..security import verify_password

import logging

router = APIRouter()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/restaurant_signup")
async def restaurant_signup(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received signup request: {data}")
    
    restaurant_user = RestaurantUserModel(**data)
    db_user = RestaurantUserService.get_user_by_email(db, email=restaurant_user.email)
    
    if db_user:
        logger.warning(f"Attempt to register with already existing email: {restaurant_user.email}")
        return {"statusCode": 400, "detail": "Email Already Registered", "response": None}
    
    created_user = RestaurantUserService.create_user(db=db, user=restaurant_user)
    logger.info(f"Restaurant user created successfully with email: {restaurant_user.email}")
    
    return {"statusCode": 200, "detail": "Added successfully", "response": created_user}

@router.post("/restaurant_login")
async def restaurant_login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received login request: {data}")
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        logger.warning("Email or password not provided in login request")
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    restaurant_user = RestaurantUserService.get_user_by_email(db, email=email)
    if not restaurant_user or not verify_password(password, restaurant_user.password):
        logger.warning(f"Failed login attempt for email: {email}")
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": restaurant_user.email})
    logger.info(f"Restaurant user logged in successfully with email: {email}")
    
    return {
        "statusCode": 200,
        "detail": "Login successful",
        "response": {
            "access_token": access_token,
            "token_type": "bearer",
            "email": restaurant_user.email,
            "phone_number": restaurant_user.phone_number,
            "id": restaurant_user.id
        }
    }

@router.get("/restaurant_user_profile/{user_id}")
async def view_profile(user_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    logger.info(f"Fetching profile for restaurant user ID: {user_id}")
    
    restaurant_user = RestaurantUserService.get_user_by_id(db, user_id=user_id)
    if not restaurant_user:
        logger.warning(f"Restaurant user ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Profile fetched for restaurant user ID: {user_id}")
    
    return {
        "statusCode": 200,
        "detail": "User profile fetched successfully",
        "response": {
            "email": restaurant_user.email,
            "phone_number": restaurant_user.phone_number
        }
    }

@router.put("/update_restaurant_user/{user_id}")
async def update_restaurant_user(user_id: int, request: Request, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    data = await request.json()
    logger.info(f"Received update request for user ID: {user_id} with data: {data}")
    
    updated_user = RestaurantUserService.update_user(db=db, user_id=user_id, update_data=data)
    if not updated_user:
        logger.warning(f"Restaurant user ID {user_id} not found or inactive")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Restaurant user ID {user_id} updated successfully")
    
    return {
        "statusCode": 200,
        "detail": "User updated successfully",
        "response": updated_user
    }

@router.delete("/delete_restaurant_user/{user_id}")
async def delete_restaurant_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    logger.info(f"Received delete request for user ID: {user_id}")
    
    deleted_user = RestaurantUserService.delete_user(db=db, user_id=user_id)
    if not deleted_user:
        logger.warning(f"Restaurant user ID {user_id} not found or inactive")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"Restaurant user ID {user_id} marked as inactive")
    
    return {
        "statusCode": 200,
        "detail": "User deleted successfully (soft delete)",
        "response": deleted_user
    }

