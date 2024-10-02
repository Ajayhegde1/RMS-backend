# app/controllers/CouponController.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..services.CouponService import CouponService
from ..database import get_db

import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/addCoupon")
async def add_coupon(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received add coupon request: {data}")

    restaurant_id = data.get("restaurant_id")
    discount_type = data.get("discount_type")
    discount = data.get("discount")
    description = data.get("description")

    if not (restaurant_id and discount_type and discount and description):
        logger.warning("Missing required fields in add coupon request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    created_coupon = CouponService.create_coupon(db=db, restaurant_id=restaurant_id, discount_type=discount_type, discount=discount, description=description)
    logger.info(f"Coupon created successfully for restaurant_id: {restaurant_id}")

    return {"statusCode": 200, "detail": "Coupon added successfully", "response": created_coupon}

@router.get("/{coupon_id}")
async def get_coupon_by_id(coupon_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching coupon details for coupon_id: {coupon_id}")

    coupon = CouponService.get_coupon_by_id(db=db, coupon_id=coupon_id)
    if not coupon:
        logger.warning(f"Coupon with ID {coupon_id} not found")
        raise HTTPException(status_code=404, detail="Coupon not found")

    logger.info(f"Coupon details fetched for coupon_id: {coupon_id}")
    return {"statusCode": 200, "detail": "Coupon fetched successfully", "response": coupon}

@router.get("/couponByRestaurantId/{restaurant_id}")
async def get_coupons_by_restaurant_id(restaurant_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching coupons for restaurant_id: {restaurant_id}")

    coupons = CouponService.get_coupons_by_restaurant_id(db=db, restaurant_id=restaurant_id)
    if not coupons:
        logger.warning(f"No coupons found for restaurant_id: {restaurant_id}")
        raise HTTPException(status_code=404, detail="No coupons found")

    logger.info(f"Coupons fetched for restaurant_id: {restaurant_id}")
    return {"statusCode": 200, "detail": "Coupons fetched successfully", "response": coupons}

@router.put("/updateCoupon/{coupon_id}")
async def update_coupon(coupon_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received update coupon request: {data}")

    updated_coupon = CouponService.update_coupon(db=db, coupon_id=coupon_id, coupon_data=data)
    if not updated_coupon:
        logger.warning(f"Coupon with ID {coupon_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Coupon not found")

    logger.info(f"Coupon ID {coupon_id} updated successfully")
    return {"statusCode": 200, "detail": "Coupon updated successfully", "response": updated_coupon}

@router.delete("/deleteCoupon/{coupon_id}")
async def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received delete coupon request for coupon_id: {coupon_id}")

    deleted_coupon = CouponService.delete_coupon(db=db, coupon_id=coupon_id)
    if not deleted_coupon:
        logger.warning(f"Coupon with ID {coupon_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Coupon not found")

    logger.info(f"Coupon ID {coupon_id} marked as inactive")
    return {"statusCode": 200, "detail": "Coupon deleted successfully (soft delete)", "response": deleted_coupon}
