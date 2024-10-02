# app/controllers/CartController.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..services.CartService import CartService
from ..database import get_db

import logging

router = APIRouter()

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/addToCart")
async def add_to_cart(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received add to cart request: {data}")

    user_id = data.get("restaurant_user_id")
    nfc_design_id = data.get("nfc_design_id")

    if not (user_id and nfc_design_id):
        logger.warning("Missing required fields in add to cart request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    result = CartService.add_to_cart(db=db, user_id=user_id, nfc_design_id=nfc_design_id)
    if result["status"] == "error":
        logger.warning(f"Add to cart failed: {result['message']}")
        raise HTTPException(status_code=400, detail=result["message"])

    logger.info("Item added to cart successfully")
    return {"statusCode": 200, "response": "Item added to cart"}

@router.post("/removeFromCart")
async def remove_from_cart(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received remove from cart request: {data}")

    user_id = data.get("restaurant_user_id")
    nfc_design_id = data.get("nfc_design_id")

    if not (user_id and nfc_design_id):
        logger.warning("Missing required fields in remove from cart request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    result = CartService.remove_from_cart(db=db, user_id=user_id, nfc_design_id=nfc_design_id)
    if result["status"] == "error":
        logger.warning(f"Remove from cart failed: {result['message']}")
        raise HTTPException(status_code=400, detail=result["message"])

    logger.info("Item removed from cart successfully")
    return {"statusCode": 200, "detail": "Soft Deleted Items from Cart", "response": "Item removed from cart"}

@router.get("/activeItems/{restaurant_user_id}")
async def get_active_items_by_user(restaurant_user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching active items for restaurant_user_id: {restaurant_user_id}")

    active_items = CartService.get_active_items_by_user_id(db=db, user_id=restaurant_user_id)
    if not active_items:
        logger.warning(f"No active items found for restaurant_user_id: {restaurant_user_id}")
        raise HTTPException(status_code=404, detail="No active items found")

    result = [{"design_name": item.nfc_design.design_name, "template_svg": item.nfc_design.template_svg} for item in active_items]
    logger.info(f"Active items fetched for restaurant_user_id: {restaurant_user_id}")
    return {"statusCode": 200, "detail": "Cart fetched successfully", "response": result}
