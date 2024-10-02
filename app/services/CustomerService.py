# app/services/CustomerService.py
from datetime import date
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..models.Customer import Customer as CustomerModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CustomerService:
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_customer(db: Session, email: str, password: str):
        customer = db.query(CustomerModel).filter(CustomerModel.email == email, CustomerModel.active == True).first()
        if customer and CustomerService.verify_password(password, customer.hashed_password):
            return customer
        return None

    @staticmethod
    def create_customer(db: Session, email: str, password: str, age: int, dob: date, phone_number: str):
        hashed_password = CustomerService.get_password_hash(password)
        customer = CustomerModel(
            email=email,
            hashed_password=hashed_password,
            age=age,
            dob=dob,
            phone_number=phone_number,
            date_added=date.today()
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def get_customer_by_id(db: Session, customer_id: int):
        return db.query(CustomerModel).filter(CustomerModel.id == customer_id, CustomerModel.active == True).first()

    @staticmethod
    def get_customer_by_email(db: Session, email: str):
        return db.query(CustomerModel).filter(CustomerModel.email == email, CustomerModel.active == True).first()

    @staticmethod
    def update_customer(db: Session, customer_id: int, update_data: dict):
        customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id, CustomerModel.active == True).first()
        if not customer:
            return None
        for key, value in update_data.items():
            setattr(customer, key, value)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id, CustomerModel.active == True).first()
        if customer:
            customer.active = False
            db.commit()
        return customer
