# app/controllers/GenerateQrController.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models.GenerateQR import GenerateQR as GenerateQrModel
from ..services.GenerateQrService import GenerateQrService
from ..database import get_db

import io
import logging

router = APIRouter()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/generateQr")
async def generate_qr(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received generate QR request: {data}")

    restaurant_user_id = data.get("restaurant_user_id")
    orientation = data.get("orientation")
    review_page_link = data.get("review_page_link")
    platform_name = data.get("platform_name")

    if not (restaurant_user_id and orientation and review_page_link and platform_name):
        logger.warning("Missing required fields in generate QR request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Check if platform exists or add it
    platform = GenerateQrService.add_platform_if_not_exists(db, platform_name)

    # Generate QR code SVG data
    qr_svg = GenerateQrService.generate_qr_svg(review_page_link)

    # Create QR data object
    qr_data = GenerateQrModel(
        review_page_link=review_page_link,
        qr_code_path=qr_svg,
        platform_name=platform.name,
        orientation=orientation,
        restaurant_user_id=restaurant_user_id
    )

    # Save QR data to the database
    created_qr = GenerateQrService.create_qr(db=db, qr_data=qr_data)
    logger.info(f"QR code generated and saved for restaurant_user_id: {restaurant_user_id}")

    return {"statusCode": 200, "detail": "QR code generated successfully", "response": created_qr.qr_code_path}

@router.get("/qrs_by_user/{restaurant_user_id}")
async def get_qrs_by_user(restaurant_user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching QR codes for restaurant_user_id: {restaurant_user_id}")

    qrs = GenerateQrService.get_qrs_by_user_id(db, restaurant_user_id)
    if not qrs:
        logger.warning(f"No QR codes found for restaurant_user_id: {restaurant_user_id}")
        raise HTTPException(status_code=404, detail="No QR codes found")

    logger.info(f"QR codes fetched for restaurant_user_id: {restaurant_user_id}")
    return {"statusCode": 200, "detail": "QR codes fetched successfully", "response": qrs}

@router.get("/qr/{qr_id}")
async def get_qr(qr_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching QR code for qr_id: {qr_id}")

    qr = GenerateQrService.get_qr_by_id(db, qr_id)
    if not qr:
        logger.warning(f"QR code with ID {qr_id} not found")
        raise HTTPException(status_code=404, detail="QR code not found")

    logger.info(f"QR code fetched for qr_id: {qr_id}")
    return {"statusCode": 200, "detail": "QR code fetched successfully", "response": qr}

@router.put("/update_qr/{qr_id}")
async def update_qr(qr_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received update request for QR code ID: {qr_id} with data: {data}")

    updated_qr = GenerateQrService.update_qr(db=db, qr_id=qr_id, update_data=data)
    if not updated_qr:
        logger.warning(f"QR code ID {qr_id} not found or inactive")
        raise HTTPException(status_code=404, detail="QR code not found")

    logger.info(f"QR code ID {qr_id} updated successfully")

    return {"statusCode": 200, "detail": "QR code updated successfully", "response": updated_qr}

@router.delete("/delete_qr/{qr_id}")
async def delete_qr(qr_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received delete request for QR code ID: {qr_id}")

    deleted_qr = GenerateQrService.delete_qr(db=db, qr_id=qr_id)
    if not deleted_qr:
        logger.warning(f"QR code ID {qr_id} not found or inactive")
        raise HTTPException(status_code=404, detail="QR code not found")

    logger.info(f"QR code ID {qr_id} marked as inactive")

    return {"statusCode": 200, "detail": "QR code deleted successfully (soft delete)", "response": deleted_qr}
