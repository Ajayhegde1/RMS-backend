# app/services/CouponService.py
import string
import random
from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..models.Coupon import Coupon as CouponModel

class CouponService:
    @staticmethod
    def generate_random_code(length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def create_coupon(db: Session, restaurant_id: int, discount_type: str, discount: int, description: str):
        expiry_date = date.today() + timedelta(days=30)
        code = CouponService.generate_random_code()
        coupon = CouponModel(
            code=code,
            discount=discount,
            discount_type=discount_type,
            description=description,
            expiry_date=expiry_date,
            active=True,
            restaurant_id=restaurant_id
        )
        db.add(coupon)
        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def get_coupon_by_id(db: Session, coupon_id: int):
        return db.query(CouponModel).filter(CouponModel.id == coupon_id, CouponModel.active == True).first()

    @staticmethod
    def get_coupons_by_restaurant_id(db: Session, restaurant_id: int):
        return db.query(CouponModel).filter(CouponModel.restaurant_id == restaurant_id, CouponModel.active == True).all()

    @staticmethod
    def redeem_coupon(db: Session, code: str):
        coupon = db.query(CouponModel).filter(CouponModel.code == code, CouponModel.active == True).first()
        if coupon:
            coupon.active = False
            db.commit()
            db.refresh(coupon)
        return coupon

    @staticmethod
    def update_coupon(db: Session, coupon_id: int, coupon_data: dict):
        coupon = db.query(CouponModel).filter(CouponModel.id == coupon_id, CouponModel.active == True).first()
        if coupon:
            for key, value in coupon_data.items():
                setattr(coupon, key, value)
            db.commit()
            db.refresh(coupon)
        return coupon

    @staticmethod
    def delete_coupon(db: Session, coupon_id: int):
        coupon = db.query(CouponModel).filter(CouponModel.id == coupon_id, CouponModel.active == True).first()
        if coupon:
            coupon.active = False
            db.commit()
            db.refresh(coupon)
        return coupon

