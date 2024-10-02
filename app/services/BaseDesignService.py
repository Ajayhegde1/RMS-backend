# app/services/BaseDesignService.py
from sqlalchemy.orm import Session
from ..models.BaseDesign import BaseDesign as BaseDesignModel
from ..models.Cuisine import Cuisine as CuisineModel

class BaseDesignService:
    @staticmethod
    def create_base_design(db: Session, base_design: BaseDesignModel):
        db.add(base_design)
        db.commit()
        db.refresh(base_design)
        return base_design

    @staticmethod
    def create_cuisine(db: Session, cuisine: CuisineModel):
        db.add(cuisine)
        db.commit()
        db.refresh(cuisine)
        return cuisine

    @staticmethod
    def get_base_designs_by_vendor_id(db: Session, vendor_id: int):
        return db.query(BaseDesignModel).filter(BaseDesignModel.vendor_id == vendor_id, BaseDesignModel.active == True).all()

    @staticmethod
    def update_base_design(db: Session, base_design_id: int, base_design_data: dict):
        base_design = db.query(BaseDesignModel).filter(BaseDesignModel.id == base_design_id, BaseDesignModel.active == True).first()
        if base_design:
            for key, value in base_design_data.items():
                setattr(base_design, key, value)
            db.commit()
            db.refresh(base_design)
        return base_design

    @staticmethod
    def delete_base_design(db: Session, base_design_id: int):
        base_design = db.query(BaseDesignModel).filter(BaseDesignModel.id == base_design_id, BaseDesignModel.active == True).first()
        if base_design:
            base_design.active = False
            db.commit()
            db.refresh(base_design)
        return base_design
