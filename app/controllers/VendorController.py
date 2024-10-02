# app/controllers/VendorController.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..services.VendorService import VendorService
from ..database import get_db
from ..utils.jwt import create_access_token
from ..middleware.jwt_middleware import JWTBearer
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register")
async def register_vendor(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    logger.info(f"Received register vendor request: {data}")

    email = data.get("email")
    password = data.get("password")
    phone_number = data.get("phone_number")
    role = data.get("role")

    if not (email and password and phone_number and role):
        logger.warning("Missing required fields in register vendor request")
        raise HTTPException(status_code=400, detail="Missing required fields")

    created_vendor = VendorService.create_vendor(db=db, email=email, password=password, phone_number=phone_number, role=role)
    logger.info(f"Vendor created successfully with email: {email}")

    return {
        "statusCode": 200,
        "detail": "Vendor registered successfully",
        "response": created_vendor
    }

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    if not (email and password):
        raise HTTPException(status_code=400, detail="Email and password are required")

    vendor = VendorService.authenticate_vendor(db, email, password)
    if not vendor:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": vendor.email, "role": vendor.role})
    vendor_details =  {
        "access_token": access_token,
        "token_type": "bearer",
        "role": vendor.role,
        "email": vendor.email,
        "phone_number": vendor.phone_number,
        "id": vendor.id
    }
    return {
        "statusCode": 200,
        "detail": "Vendor retrieved successfully",
        "response": vendor_details
    }

@router.get("/{vendor_id}")
async def get_vendor_by_id(vendor_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    vendor = VendorService.get_vendor_by_id(db=db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {
        "statusCode": 200,
        "detail": "Vendor retrieved successfully",
        "response": vendor
    }

@router.put("/update/{vendor_id}")
async def update_vendor(vendor_id: int, request: Request, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    data = await request.json()
    updated_vendor = VendorService.update_vendor(db=db, vendor_id=vendor_id, **data)
    if not updated_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found or inactive")
    return {
        "statusCode": 200,
        "detail": "Vendor updated successfully",
        "response": updated_vendor
    }

@router.delete("/delete/{vendor_id}")
async def delete_vendor(vendor_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    deleted_vendor = VendorService.delete_vendor(db=db, vendor_id=vendor_id)
    if not deleted_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {
        "statusCode": 200,
        "detail": "Vendor deleted successfully (soft delete)",
        "response": deleted_vendor
    }

