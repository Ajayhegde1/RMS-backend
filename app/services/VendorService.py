# app/services/VendorService.py
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..models.Vendor import Vendor as VendorModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class VendorService:
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_vendor(db: Session, email: str, password: str):
        vendor = db.query(VendorModel).filter(VendorModel.email == email, VendorModel.active == True).first()  # **Add filter for active**
        if vendor and VendorService.verify_password(password, vendor.hashed_password):
            return vendor
        return None

    @staticmethod
    def create_vendor(db: Session, email: str, password: str, phone_number: str, role: str):
        hashed_password = VendorService.get_password_hash(password)
        vendor = VendorModel(
            email=email,
            hashed_password=hashed_password,
            phone_number=phone_number,
            role=role
        )
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
        return vendor

    @staticmethod
    def get_vendor_by_id(db: Session, vendor_id: int):
        return db.query(VendorModel).filter(VendorModel.id == vendor_id, VendorModel.active == True).first()  # **Add filter for active**

    @staticmethod
    def get_vendor_by_email(db: Session, email: str):
        return db.query(VendorModel).filter(VendorModel.email == email, VendorModel.active == True).first()  # **Add filter for active**

    @staticmethod
    def update_vendor(db: Session, vendor_id: int, **kwargs):
        vendor = db.query(VendorModel).filter(VendorModel.id == vendor_id, VendorModel.active == True).first()  # **Add filter for active**
        if not vendor:
            return None
        for key, value in kwargs.items():
            setattr(vendor, key, value)
        db.commit()
        db.refresh(vendor)
        return vendor

    @staticmethod
    def delete_vendor(db: Session, vendor_id: int):
        vendor = db.query(VendorModel).filter(VendorModel.id == vendor_id).first()
        if not vendor:
            return None
        vendor.active = False
        db.commit()
        return vendor

