from sqlalchemy.orm import Session
from ..models.Restaurant import Restaurant as RestaurantModel

class RestaurantService:
    @staticmethod
    def create_restaurant(db: Session, restaurant: RestaurantModel):
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        return restaurant
    
    @staticmethod
    def get_restaurant_by_id(db: Session, restaurant_id: int):
        return db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id, RestaurantModel.active == True).first()

    @staticmethod
    def get_restaurant_by_user_id(db: Session, restaurant_user_id: int):
        return db.query(RestaurantModel).filter(RestaurantModel.restaurant_user_id == restaurant_user_id, RestaurantModel.active == True).first()

    @staticmethod
    def update_restaurant(db: Session, restaurant_id: int, update_data: dict):
        restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id, RestaurantModel.active == True).first()
        if not restaurant:
            return None
        for key, value in update_data.items():
            setattr(restaurant, key, value)
        db.commit()
        db.refresh(restaurant)
        return restaurant

    @staticmethod
    def delete_restaurant(db: Session, restaurant_id: int):
        restaurant = db.query(RestaurantModel).filter(RestaurantModel.id == restaurant_id, RestaurantModel.active == True).first()
        if restaurant:
            restaurant.active = False
            db.commit()
        return restaurant
