from sqlalchemy.orm import Session
from ..models.RawMaterial import RawMaterial as RawMaterialModel
from ..models.RawMaterialCategory import RawMaterialCategory as CategoryModel

class RawMaterialService:
    @staticmethod
    def create_raw_material(db: Session, name: str, quantity: int, price: float, category_id: int, unit: str, restaurant_id: int):
        raw_material = RawMaterialModel(
            name=name, 
            quantity=quantity, 
            price=price, 
            category_id=category_id, 
            unit=unit, 
            restaurant_id=restaurant_id
        )
        db.add(raw_material)
        db.commit()
        db.refresh(raw_material)
        return raw_material

    @staticmethod
    def get_all_raw_materials(db: Session):
        return db.query(RawMaterialModel).all()

    @staticmethod
    def get_raw_material_by_id(db: Session, raw_material_id: int):
        return db.query(RawMaterialModel).filter(RawMaterialModel.id == raw_material_id).first()

    @staticmethod
    def get_raw_material_by_name(db: Session, name: str, restaurant_id: int):
        return db.query(RawMaterialModel).filter(RawMaterialModel.name == name, RawMaterialModel.restaurant_id == restaurant_id).all()

    @staticmethod
    def create_or_get_category(db: Session, name: str):
        category = db.query(CategoryModel).filter(CategoryModel.name == name).first()
        if not category:
            category = CategoryModel(name=name)
            db.add(category)
            db.commit()
            db.refresh(category)
        return category

    @staticmethod
    def get_all_raw_materials_by_restaurant(db: Session, restaurant_id: int):
        return db.query(RawMaterialModel, CategoryModel.name.label('category_name')).join(CategoryModel, RawMaterialModel.category_id == CategoryModel.id).filter(RawMaterialModel.restaurant_id == restaurant_id).all()