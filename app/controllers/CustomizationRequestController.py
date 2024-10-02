#app/controllers/CustomizationRequestController.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models.CustomizationRequest import CustomizationRequest as CustomizationRequestModel
from ..services.CustomizationRequestService import CustomizationRequestService
from ..services.RestaurantUserService import RestaurantUserService
from ..database import get_db

import logging

router = APIRouter()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/add_customization_request")
async def add_customization_request(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received customization request: {data}")

    details = data.get("details")
    restaurant_user_id = data.get("restaurant_user_id")

    # Verify if the restaurant user exists
    restaurant_user = RestaurantUserService.get_user_by_id(db, restaurant_user_id)
    if not restaurant_user:
        logger.warning(f"Restaurant user ID {restaurant_user_id} not found")
        raise HTTPException(status_code=404, detail="Restaurant user not found")

    # Create customization request entry
    customization_request = CustomizationRequestModel(
        details=details,
        restaurant_user_id=restaurant_user_id
    )
    db_customization_request = CustomizationRequestService.create_customization_request(db=db, customization_request=customization_request)
    logger.info(f"Customization request created successfully with ID: {db_customization_request.id}")

    return {"statusCode": 200, "detail": "Customization request added successfully", "response": db_customization_request.id}

@router.get("/customization_request/{request_id}")
async def get_customization_request(request_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching customization request details for ID: {request_id}")

    customization_request = CustomizationRequestService.get_customization_request_by_id(db, request_id)
    if not customization_request:
        logger.warning(f"Customization request ID {request_id} not found")
        raise HTTPException(status_code=404, detail="Customization request not found")

    logger.info(f"Customization request details fetched for ID: {request_id}")

    return {
        "statusCode": 200,
        "detail": "Customization request fetched successfully",
        "response": {
            "details": customization_request.details,
            "restaurant_user_id": customization_request.restaurant_user_id
        }
    }

@router.put("/update_customization_request/{request_id}")
async def update_customization_request(request_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received update request for customization request ID: {request_id} with data: {data}")

    updated_customization_request = CustomizationRequestService.update_customization_request(db=db, request_id=request_id, update_data=data)
    if not updated_customization_request:
        logger.warning(f"Customization request ID {request_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Customization request not found")

    logger.info(f"Customization request ID {request_id} updated successfully")

    return {"statusCode": 200, "detail": "Customization request updated successfully", "response": updated_customization_request}

@router.delete("/delete_customization_request/{request_id}")
async def delete_customization_request(request_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received delete request for customization request ID: {request_id}")

    deleted_customization_request = CustomizationRequestService.delete_customization_request(db=db, request_id=request_id)
    if not deleted_customization_request:
        logger.warning(f"Customization request ID {request_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Customization request not found")

    logger.info(f"Customization request ID {request_id} marked as inactive")

    return {"statusCode": 200, "detail": "Customization request deleted successfully (soft delete)", "response": deleted_customization_request}
