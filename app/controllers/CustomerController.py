# app/controllers/CustomerController.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..services.CustomerService import CustomerService
from ..database import get_db
from ..utils.jwt import create_access_token
from ..middleware.jwt_middleware import JWTBearer
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/addCustomer")
async def add_customer(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received add customer request: {data}")

    email = data.get("email")
    password = data.get("password")
    age = data.get("age")
    dob_str = data.get("dob")
    phone_number = data.get("phone_number")

    if not (email and password and age and dob_str and phone_number):
        logger.warning("Missing required fields in add customer request")
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    
    created_customer = CustomerService.create_customer(db=db, email=email, password=password, age=age, dob=dob, phone_number=phone_number)
    logger.info(f"Customer created successfully with email: {email}")

    return {
        "statusCode": 200,
        "detail": "Customer added successfully",
        "response": created_customer
    }

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    if not (email and password):
        raise HTTPException(status_code=400, detail="Email and password are required")

    customer = CustomerService.authenticate_customer(db, email, password)
    if not customer:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": customer.email})
    return {
        "statusCode": 200,
        "detail": "Login successful",
        "response": {
            "access_token": access_token,
            "token_type": "bearer",
            "email": customer.email,
            "phone_number": customer.phone_number,
            "id": customer.id
        }
    }

@router.get("/{customer_id}")
async def get_customer_by_id(customer_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    logger.info(f"Fetching customer details for customer_id: {customer_id}")
    customer = CustomerService.get_customer_by_id(db=db, customer_id=customer_id)
    if not customer:
        logger.warning(f"Customer with ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")

    logger.info(f"Customer details fetched for customer_id: {customer_id}")
    return {"statusCode": 200, "detail": "Customer fetched successfully", "response": customer}

@router.put("/update_customer/{customer_id}")
async def update_customer(customer_id: int, request: Request, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    data = await request.json()
    logger.info(f"Received update request for customer ID: {customer_id} with data: {data}")

    updated_customer = CustomerService.update_customer(db=db, customer_id=customer_id, update_data=data)
    if not updated_customer:
        logger.warning(f"Customer ID {customer_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Customer not found")

    logger.info(f"Customer ID {customer_id} updated successfully")

    return {"statusCode": 200, "detail": "Customer updated successfully", "response": updated_customer}

@router.delete("/delete_customer/{customer_id}")
async def delete_customer(customer_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    logger.info(f"Received delete request for customer ID: {customer_id}")

    deleted_customer = CustomerService.delete_customer(db=db, customer_id=customer_id)
    if not deleted_customer:
        logger.warning(f"Customer ID {customer_id} not found or inactive")
        raise HTTPException(status_code=404, detail="Customer not found")

    logger.info(f"Customer ID {customer_id} marked as inactive")

    return {"statusCode": 200, "detail": "Customer deleted successfully (soft delete)", "response": deleted_customer}

