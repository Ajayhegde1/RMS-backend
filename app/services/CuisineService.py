# app/services/CuisineService.py
from sqlalchemy.orm import Session
from ..models.Cuisine import Cuisine as CuisineModel

class CuisineService:
    @staticmethod
    def create_cuisine(db: Session, cuisine_data: CuisineModel):
        db.add(cuisine_data)
        db.commit()
        db.refresh(cuisine_data)
        return cuisine_data

    @staticmethod
    def get_cuisines_by_base_design_id(db: Session, base_design_id: int):
        return db.query(CuisineModel).filter(CuisineModel.base_design_id == base_design_id, CuisineModel.active == True).all()
    
    @staticmethod
    def update_cuisine(db: Session, cuisine_id: int, cuisine_data: dict):
        cuisine = db.query(CuisineModel).filter(CuisineModel.id == cuisine_id, CuisineModel.active == True).first()
        if cuisine:
            for key, value in cuisine_data.items():
                setattr(cuisine, key, value)
            db.commit()
            db.refresh(cuisine)
        return cuisine

    @staticmethod
    def delete_cuisine(db: Session, cuisine_id: int):
        cuisine = db.query(CuisineModel).filter(CuisineModel.id == cuisine_id, CuisineModel.active == True).first()
        if cuisine:
            cuisine.active = False
            db.commit()
            db.refresh(cuisine)
        return cuisine

