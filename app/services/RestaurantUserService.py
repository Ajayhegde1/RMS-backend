# app/services/RestaurantUserService.py
from sqlalchemy.orm import Session
from ..models.RestaurantUser import RestaurantUser as RestaurantUserModel
from ..security import get_password_hash

class RestaurantUserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(RestaurantUserModel).filter(RestaurantUserModel.email == email, RestaurantUserModel.active == True).first()

    @staticmethod
    def create_user(db: Session, user: RestaurantUserModel):
        hashed_password = get_password_hash(user.password)
        db_user = RestaurantUserModel(email=user.email, password=hashed_password, phone_number=user.phone_number)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(RestaurantUserModel).filter(RestaurantUserModel.id == user_id, RestaurantUserModel.active == True).first()

    @staticmethod
    def update_user(db: Session, user_id: int, update_data: dict):
        user = db.query(RestaurantUserModel).filter(RestaurantUserModel.id == user_id, RestaurantUserModel.active == True).first()
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(RestaurantUserModel).filter(RestaurantUserModel.id == user_id, RestaurantUserModel.active == True).first()
        if user:
            user.active = False
            db.commit()
        return user

