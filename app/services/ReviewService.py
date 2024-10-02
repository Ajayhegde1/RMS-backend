# app/services/ReviewService.py
from sqlalchemy.orm import Session
from ..models.Review import Review as ReviewModel
from datetime import date

class ReviewService:
    @staticmethod
    def create_review(db: Session, name: str, dob: date, age: int, phone_number: str, email_id: str, restaurant_id: int):
        review = ReviewModel(
            name=name,
            dob=dob,
            age=age,
            phone_number=phone_number,
            email_id=email_id,
            restaurant_id=restaurant_id
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def get_review_by_id(db: Session, review_id: int):
        return db.query(ReviewModel).filter(ReviewModel.id == review_id, ReviewModel.active == True).first()  # **Add filter for active**

    @staticmethod
    def get_reviews_by_restaurant_id(db: Session, restaurant_id: int):
        return db.query(ReviewModel).filter(ReviewModel.restaurant_id == restaurant_id, ReviewModel.active == True).all()  # **Add filter for active**

    @staticmethod
    def update_review(db: Session, review_id: int, **kwargs):
        review = db.query(ReviewModel).filter(ReviewModel.id == review_id, ReviewModel.active == True).first()  # **Add filter for active**
        if not review:
            return None
        for key, value in kwargs.items():
            setattr(review, key, value)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def delete_review(db: Session, review_id: int):
        review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
        if not review:
            return None
        review.active = False
        db.commit()
        return review
