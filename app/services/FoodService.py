# app/services/FoodService.py
from sqlite3 import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.Food import Food as FoodModel
from ..models.FoodRawMaterial import FoodRawMaterial as FoodRawMaterialModel
from ..models.RawMaterial import RawMaterial as RawMaterialModel

class FoodService:
    @staticmethod
    def create_food(
        db: Session, 
        name: str, 
        restaurant_id: int, 
        category: str = None, 
        is_veg: bool = None, 
        cuisine: str = None, 
        description: str = None, 
        rating: float = None, 
        nutritional_value: str = None, 
        price: float = None, 
        image: str = None, 
        youtube_link: str = None
    ):
        # Check if the food item already exists for the same restaurant and category
        existing_food = db.query(FoodModel).filter(
            FoodModel.name == name,
            FoodModel.restaurant_id == restaurant_id,
            FoodModel.category == category
        ).first()
        
        if existing_food:
            raise HTTPException(status_code=400, detail="Food item with this name already exists for this restaurant and category")

        try:
            food = FoodModel(
                name=name,
                restaurant_id=restaurant_id,
                category=category,
                is_veg=is_veg,
                cuisine=cuisine,
                description=description,
                rating=rating,
                nutritional_value=nutritional_value,
                price=price,
                image=image,
                youtube_link=youtube_link
            )
            db.add(food)
            db.commit()
            db.refresh(food)
            return food
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Failed to create food item due to a database integrity error")

    @staticmethod
    def add_raw_material_to_food(db: Session, food_id: int, raw_material_id: int, quantity: float):
        food_raw_material = FoodRawMaterialModel(
            food_id=food_id,
            raw_material_id=raw_material_id,
            quantity=quantity
        )
        db.add(food_raw_material)
        db.commit()
        db.refresh(food_raw_material)
        return food_raw_material

    @staticmethod
    def get_food_by_id(db: Session, food_id: int):
        food = db.query(FoodModel).filter(FoodModel.id == food_id).first()
        if not food:
            return None
        
        raw_materials = db.query(FoodRawMaterialModel, RawMaterialModel).join(RawMaterialModel, FoodRawMaterialModel.raw_material_id == RawMaterialModel.id).filter(FoodRawMaterialModel.food_id == food_id).all()
        
        return {
            "food": food,
            "raw_materials": [{"name": rm.name, "quantity": frm.quantity} for frm, rm in raw_materials]
        }

    @staticmethod
    def get_all_food_by_restaurant(db: Session, restaurant_id: int):
        foods = db.query(FoodModel).filter(FoodModel.restaurant_id == restaurant_id).all()
        # return [{"name": food.name, "image": food.image, "is_veg": food.is_veg, "price": food.price, "description": food.description} for food in foods]
        return foods

    @staticmethod
    def update_food(db: Session, food_id: int, name: str = None, category: str = None, is_veg: bool = None, cuisine: str = None, description: str = None, rating: float = None, nutritional_value: str = None, price: float = None, image: str = None, youtube_link: str = None):
        food = db.query(FoodModel).filter(FoodModel.id == food_id).first()
        if not food:
            return None

        if name:
            food.name = name
        if category:
            food.category = category
        if is_veg is not None:
            food.is_veg = is_veg
        if cuisine:
            food.cuisine = cuisine
        if description:
            food.description = description
        if rating is not None:
            food.rating = rating
        if nutritional_value:
            food.nutritional_value = nutritional_value
        if price is not None:
            food.price = price
        if image:
            food.image = image
        if youtube_link:
            food.youtube_link = youtube_link

        db.commit()
        db.refresh(food)
        return food

    @staticmethod
    def delete_food(db: Session, food_id: int):
        # Delete all FoodRawMaterial instances with the given food_id
        db.query(FoodRawMaterialModel).filter(FoodRawMaterialModel.food_id == food_id).delete()

        # Find the food item
        food = db.query(FoodModel).filter(FoodModel.id == food_id).first()
        if not food:
            return None

        # Delete the food item
        db.delete(food)
        db.commit()
        return food