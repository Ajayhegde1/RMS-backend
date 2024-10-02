# app/controllers/ReviewController.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..services.ReviewService import ReviewService
from ..database import get_db
from datetime import datetime

import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/addReview")
async def add_review(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received add review request: {data}")

    name = data.get("name")
    dob_str = data.get("dob")
    age = data.get("age")
    phone_number = data.get("phone_number")
    email_id = data.get("email_id")
    restaurant_id = data.get("restaurant_id")

    if not (name and dob_str and age and phone_number and email_id and restaurant_id):
        logger.warning("Missing required fields in add review request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
    except ValueError:
        logger.warning("Invalid date format for dob in add review request")
        raise HTTPException(status_code=400, detail="Invalid date format")

    created_review = ReviewService.create_review(db=db, name=name, dob=dob, age=age, phone_number=phone_number, email_id=email_id, restaurant_id=restaurant_id)
    logger.info(f"Review created successfully for restaurant_id: {restaurant_id}")

    return {
        "statusCode": 200,
        "detail": "Review added successfully",
        "response": created_review
    }

@router.get("/{review_id}")
async def get_review_by_id(review_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching review details for review_id: {review_id}")

    review = ReviewService.get_review_by_id(db=db, review_id=review_id)
    if not review:
        logger.warning(f"Review with ID {review_id} not found")
        raise HTTPException(status_code=404, detail="Review not found")

    logger.info(f"Review details fetched for review_id: {review_id}")
    return {
        "statusCode": 200,
        "detail": "Review details retrieved",
        "response": review
    }

@router.get("/reviewsByRestaurantId/{restaurant_id}")
async def get_reviews_by_restaurant_id(restaurant_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching reviews for restaurant_id: {restaurant_id}")

    reviews = ReviewService.get_reviews_by_restaurant_id(db=db, restaurant_id=restaurant_id)
    if not reviews:
        logger.warning(f"No reviews found for restaurant_id: {restaurant_id}")
        raise HTTPException(status_code=404, detail="No reviews found")

    logger.info(f"Reviews fetched for restaurant_id: {restaurant_id}")
    return {
        "statusCode": 200,
        "detail": "Reviews retrieved",
        "response": reviews
    }

@router.put("/updateReview/{review_id}")
async def update_review(review_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received update review request for review_id {review_id}: {data}")

    name = data.get("name")
    dob_str = data.get("dob")
    age = data.get("age")
    phone_number = data.get("phone_number")
    email_id = data.get("email_id")

    dob = None
    if dob_str:
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            logger.warning("Invalid date format for dob in update review request")
            raise HTTPException(status_code=400, detail="Invalid date format")

    updated_review = ReviewService.update_review(db=db, review_id=review_id, name=name, dob=dob, age=age, phone_number=phone_number, email_id=email_id)
    if not updated_review:
        logger.warning(f"Review with ID {review_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Review not found or inactive")

    logger.info(f"Review updated successfully for review_id: {review_id}")
    return {
        "statusCode": 200,
        "detail": "Review updated successfully",
        "response": updated_review
    }

@router.delete("/deleteReview/{review_id}")
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received delete review request for review_id {review_id}")

    deleted_review = ReviewService.soft_delete_review(db=db, review_id=review_id)
    if not deleted_review:
        logger.warning(f"Review with ID {review_id} not found or already inactive")
        raise HTTPException(status_code=404, detail="Review not found or already inactive")

    logger.info(f"Review soft deleted successfully for review_id: {review_id}")
    return {
        "statusCode": 200,
        "detail": "Review deleted successfully (soft delete)",
        "response": deleted_review
    }

